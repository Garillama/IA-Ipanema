"""Transporte de tarea al gateway existente; el worker solo monta su socket."""
import os
import socketserver
import threading

from .gateway import Gateway, serve
from ..core import IpanemaError


class TaskBroker:
    def __init__(self, project, grant_id, path):
        self.events = []
        events = self.events
        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                gateway = Gateway(project, grant_id)
                class Observed:
                    def tools(self):
                        tools = gateway.tools()
                        events.append({'event': 'tools/list', 'tools': [t['name'] for t in tools]})
                        return tools
                    def call(self, name, arguments):
                        try:
                            result = gateway.call(name, arguments)
                        except IpanemaError as exc:
                            events.append({'event': 'tools/call', 'tool': name, 'status': 'failed',
                                'category': 'timeout' if str(exc) == 'provider_operation_failed:TimeoutExpired' else 'gateway_operation_failed'})
                            raise
                        events.append({'event': 'tools/call', 'tool': name, 'status': result.get('status')})
                        return result
                    def close(self):
                        gateway.close()
                with self.connection.makefile('r', encoding='utf-8') as source, self.connection.makefile('w', encoding='utf-8') as destination:
                    serve(Observed(), source, destination)
        self.server = socketserver.UnixStreamServer(str(path), Handler)
        os.chmod(path, 0o600)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
