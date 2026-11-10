#!/usr/bin/env python3
"""Transporte stdio hacia el socket de una tarea; no accede a política ni OAuth."""
import argparse
import socket
import sys
import threading


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', required=True)
    args = parser.parse_args()
    with socket.socket(socket.AF_UNIX) as channel:
        channel.connect(args.socket)
        def forward():
            try:
                for line in sys.stdin.buffer:
                    if len(line) > 4_000_000:
                        break
                    channel.sendall(line)
                channel.shutdown(socket.SHUT_WR)
            except OSError:
                pass
        threading.Thread(target=forward, daemon=True).start()
        while True:
            chunk = channel.recv(65536)
            if not chunk:
                break
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()


if __name__ == '__main__':
    main()
