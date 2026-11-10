"""Cliente stdio MCP acotado, sin SDK adicional ni registros de respuestas crudas."""
from __future__ import annotations

import json
import os
import queue
import signal
import subprocess
import threading
import time

from ..core import IpanemaError

MAX_MESSAGE = 4_000_000


class StdioClient:
    def __init__(self, command, *, cwd, env, timeout=45):
        self.timeout, self.sequence = timeout, 0
        self.messages = queue.Queue(maxsize=64)
        self.process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                        start_new_session=True)
        threading.Thread(target=self._reader, daemon=True).start()
        try:
            self.initialized = self.request('initialize', {
                'protocolVersion': '2025-06-18', 'capabilities': {},
                'clientInfo': {'name': 'ia-ipanema-access', 'version': '1.0.0'}})
            self.notify('notifications/initialized', {})
        except Exception:
            self.close()
            raise

    def _reader(self):
        try:
            while True:
                line = self.process.stdout.readline(MAX_MESSAGE + 1)
                if not line:
                    self.messages.put_nowait(None)
                    return
                if len(line) > MAX_MESSAGE:
                    self.messages.put_nowait(None)
                    return
                self.messages.put_nowait(json.loads(line))
        except (ValueError, OSError, queue.Full):
            try:
                self.messages.put_nowait(None)
            except queue.Full:
                pass

    def _send(self, message):
        try:
            self.process.stdin.write((json.dumps(message, allow_nan=False) + '\n').encode())
            self.process.stdin.flush()
        except (OSError, ValueError):
            raise IpanemaError('mcp_transport_closed') from None

    def notify(self, method, params):
        self._send({'jsonrpc': '2.0', 'method': method, 'params': params})

    def request(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        self._send({'jsonrpc': '2.0', 'id': request_id, 'method': method, 'params': params})
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                response = self.messages.get(timeout=max(.01, deadline - time.monotonic()))
            except queue.Empty:
                self.close()
                raise IpanemaError('mcp_timeout') from None
            if not isinstance(response, dict):
                raise IpanemaError('mcp_invalid_or_closed')
            if 'method' in response and 'id' in response:
                self._send({'jsonrpc': '2.0', 'id': response['id'], 'error': {
                    'code': -32601, 'message': 'Client method unsupported'}})
            if response.get('id') == request_id:
                if 'error' in response or not isinstance(response.get('result'), dict):
                    raise IpanemaError('mcp_request_failed')
                return response['result']
            if time.monotonic() >= deadline:
                self.close()
                raise IpanemaError('mcp_timeout')

    def tools(self):
        tools, cursor = [], None
        for _ in range(10):
            result = self.request('tools/list', {'cursor': cursor} if cursor else {})
            if not isinstance(result.get('tools'), list):
                raise IpanemaError('mcp_tools_schema_changed')
            tools.extend(result['tools'])
            cursor = result.get('nextCursor')
            if not cursor:
                return tools
        raise IpanemaError('mcp_tools_pagination_limit')

    def call(self, name, arguments):
        result = self.request('tools/call', {'name': name, 'arguments': arguments})
        if result.get('isError'):
            raise IpanemaError('mcp_tool_failed')
        return result

    def close(self):
        if self.process.poll() is None:
            try:
                os.killpg(self.process.pid, signal.SIGTERM)
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(self.process.pid, signal.SIGKILL)
                self.process.wait(timeout=5)
        for pipe in (self.process.stdin, self.process.stdout):
            if pipe:
                pipe.close()
