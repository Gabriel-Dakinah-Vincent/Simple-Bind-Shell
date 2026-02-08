# Bind Shell

A lightweight, production-ready bind shell implementation in Python with comprehensive CLI support, logging, and error handling.

[![CI](https://github.com/yourusername/bind-shell/workflows/CI/badge.svg)](https://github.com/yourusername/bind-shell/actions)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage Guide](#usage-guide)
- [Best Practices](#best-practices)
- [Security Considerations](#security-considerations)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

- **Multi-threaded Architecture**: Handle multiple concurrent client connections
- **Robust Error Handling**: Comprehensive exception handling and logging
- **Timeout Protection**: Command execution (30s) and client connection (5min) timeouts
- **Graceful Shutdown**: Clean resource cleanup on Ctrl+C
- **Configurable**: Flexible host, port, and connection limit settings
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Production-Ready**: Logging, monitoring, and error recovery built-in
- **CLI Interface**: User-friendly command-line interface with click
- **Well-Tested**: Comprehensive test suite with pytest

## Installation

### From PyPI (Recommended)

```bash
pip install bind-shell
```

### From Source

```bash
git clone https://github.com/yourusername/bind-shell.git
cd bind-shell
pip install -e .
```

### Development Installation

For contributors and developers:

```bash
git clone https://github.com/yourusername/bind-shell.git
cd bind-shell
pip install -e ".[dev]"
```

This installs additional tools: pytest, black, ruff, coverage.

## Quick Start

### 1. Start the Server

```bash
# Start with defaults (0.0.0.0:4444)
bind-shell
```

### 2. Connect from Client

```bash
# Using netcat
nc localhost 4444

# Using telnet
telnet localhost 4444
```

### 3. Execute Commands

```bash
ls -la
pwd
whoami
exit
```

## Architecture

### Package Structure

```
bind-shell/
├── src/simple_bind_shell/    # Source code (src-layout)
│   ├── __init__.py            # Package initialization and public API
│   ├── version.py             # Version management
│   ├── bind_shell.py          # Core bind shell logic
│   └── cli.py                 # Command-line interface
├── tests/                     # Test suite
├── docs/                      # Documentation
└── pyproject.toml             # Project metadata and dependencies
```

### Core Components

#### BindShell Class

The main class implementing bind shell functionality:

- **Initialization**: Configures host, port, and connection limits
- **Command Execution**: Runs shell commands via subprocess
- **Client Handling**: Manages individual client connections in separate threads
- **Server Loop**: Accepts and dispatches incoming connections

#### CLI Module

Provides command-line interface using Click:

- Argument parsing and validation
- Help text and version information
- Integration with BindShell class

### Design Principles

1. **Modularity**: Separate concerns (core logic, CLI, tests)
2. **Testability**: Class-based design enables unit testing
3. **Standards Compliance**: Follows PEP 621 and modern packaging standards
4. **Extensibility**: Easy to add features like authentication or encryption
5. **Minimal Dependencies**: Only requires click for CLI functionality

### Threading Model

- Main thread: Accepts incoming connections
- Worker threads: Handle individual client sessions (daemon threads)
- Thread-safe: Each client has isolated socket and state

### Protocol

Simple text-based protocol:
1. Client connects to server
2. Client sends commands terminated by newline
3. Server executes command and returns output
4. Client sends "exit" to close connection

## Usage Guide

### Command-Line Interface

#### Basic Usage

```bash
# Start with default settings
bind-shell

# Output:
# [*] Bind shell listening on 0.0.0.0:4444
# [*] Max connections: 10
# [*] Press Ctrl+C to stop
```

#### Host Configuration

```bash
# Listen on all interfaces (default)
bind-shell --host 0.0.0.0

# Listen on localhost only (recommended for testing)
bind-shell --host 127.0.0.1

# Listen on specific IP
bind-shell --host 192.168.1.100
```

#### Port Configuration

```bash
# Default port
bind-shell --port 4444

# Custom port
bind-shell --port 8080

# High port (no root required)
bind-shell --port 9999
```

#### Connection Limits

```bash
# Allow up to 50 queued connections
bind-shell --max-connections 50

# Minimal setup (1 connection at a time)
bind-shell --max-connections 1
```

#### Verbose Logging

```bash
# Enable debug logging
bind-shell --verbose

# Combine with other options
bind-shell --host 127.0.0.1 --port 9999 --verbose

# Save logs to file
bind-shell --verbose 2>&1 | tee server.log
```

#### Help and Version

```bash
# Show help
bind-shell --help

# Show version
bind-shell --version
```

### Python Module Usage

#### Basic Example

```python
from simple_bind_shell import BindShell

# Create instance with defaults
shell = BindShell()

# Start the server (blocking)
shell.start()
```

#### Custom Configuration

```python
from simple_bind_shell import BindShell

# Configure custom settings
shell = BindShell(
    host="127.0.0.1",
    port=5555,
    max_connections=20
)

shell.start()
```

#### Non-Blocking Server

```python
import threading
from simple_bind_shell import BindShell

# Run server in background thread
shell = BindShell(host="127.0.0.1", port=4444)
thread = threading.Thread(target=shell.start, daemon=True)
thread.start()

# Do other work here
import time
time.sleep(60)

# Stop the server
shell.stop()
```

#### Error Handling

```python
from simple_bind_shell import BindShell, BindShellError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

try:
    shell = BindShell(host="0.0.0.0", port=80)  # Privileged port
    shell.start()
except BindShellError as e:
    print(f"Failed to start server: {e}")
except KeyboardInterrupt:
    print("Server stopped by user")
```

#### Command Execution

```python
from simple_bind_shell import BindShell

shell = BindShell()

# Execute single command
result = shell.run_command("echo Hello World")
print(result.decode())  # Output: Hello World

# Handle errors
result = shell.run_command("invalid_command")
if b"Error" in result:
    print("Command failed")
```

#### Logging Integration

```python
import logging
from simple_bind_shell import BindShell

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bind_shell.log'),
        logging.StreamHandler()
    ]
)

# Start server
shell = BindShell(host="127.0.0.1", port=4444)
shell.start()
```

### Client Connection Examples

#### Using Netcat (Linux/macOS)

```bash
# Connect to server
nc localhost 4444

# Execute commands
ls -la
pwd
id
exit
```

#### Using Netcat (Windows)

```cmd
ncat localhost 4444
```

#### Using Telnet

```bash
telnet localhost 4444
```

#### Using Python Client

```python
import socket

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 4444))

# Receive welcome message
print(client.recv(1024).decode())

# Send command
client.sendall(b"whoami\n")
print(client.recv(4096).decode())

# Close connection
client.sendall(b"exit\n")
client.close()
```

### Advanced Usage

#### Running as System Service (systemd)

Create `/etc/systemd/system/bind-shell.service`:

```ini
[Unit]
Description=Bind Shell Server
After=network.target

[Service]
Type=simple
User=bindshell
ExecStart=/usr/local/bin/bind-shell --host 127.0.0.1 --port 4444
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bind-shell
sudo systemctl start bind-shell
sudo systemctl status bind-shell
```

#### Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

RUN pip install bind-shell

EXPOSE 4444

CMD ["bind-shell", "--host", "0.0.0.0", "--port", "4444"]
```

Build and run:

```bash
docker build -t bind-shell .
docker run -p 4444:4444 bind-shell
```

#### Environment Variables

```bash
# Set defaults via environment
export BIND_SHELL_HOST=127.0.0.1
export BIND_SHELL_PORT=5555

# Use in script
bind-shell --host $BIND_SHELL_HOST --port $BIND_SHELL_PORT
```

#### Process Management

```bash
# Run in background
bind-shell &

# Get PID
echo $!

# Kill process
kill <PID>

# Run with nohup
nohup bind-shell --verbose > bind-shell.log 2>&1 &
```

## Best Practices

### Security Best Practices

#### Network Security

**1. Restrict Network Access**

```bash
# Always bind to localhost for local testing
bind-shell --host 127.0.0.1  # Recommended

# Avoid on production systems
# bind-shell --host 0.0.0.0
```

**Use firewall rules:**
```bash
# Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 4444 -s 192.168.1.100 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 4444 -j DROP

# Linux (ufw)
sudo ufw allow from 192.168.1.100 to any port 4444
sudo ufw deny 4444

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

**Network segmentation:**
```bash
# Use VLANs or separate networks
# Bind to internal network interface only
bind-shell --host 10.0.1.100 --port 4444
```

**2. Use Non-Privileged Ports**

```bash
# Good: Ports > 1024 (no root required)
bind-shell --port 4444
bind-shell --port 8080
bind-shell --port 9999

# Bad: Privileged ports (require root)
# bind-shell --port 80
# bind-shell --port 443
```

**3. Implement Access Controls**

```bash
# Create dedicated user without login shell
sudo useradd -r -s /bin/false bindshell

# Run as dedicated user
sudo -u bindshell bind-shell --host 127.0.0.1
```

**Use SELinux/AppArmor:**
```bash
# SELinux context
sudo semanage port -a -t bindshell_port_t -p tcp 4444

# AppArmor profile
sudo aa-enforce /etc/apparmor.d/usr.local.bin.bind-shell
```

#### Application Security

**1. Input Validation**

The application validates inputs automatically:
```bash
# Port validation (1-65535)
bind-shell --port 70000  # Will fail

# Connection limits (1-100)
bind-shell --max-connections 200  # Will fail
```

**2. Command Execution Safety**

Avoid dangerous commands in client sessions:
```bash
# Dangerous - avoid these:
rm -rf /
dd if=/dev/zero of=/dev/sda
:(){ :|:& };:  # Fork bomb
```

Built-in timeouts:
- Command timeout: 30 seconds
- Connection timeout: 5 minutes

**3. Logging and Monitoring**

```bash
# Log to file
bind-shell --verbose 2>&1 | tee /var/log/bind-shell.log

# Log with timestamps
bind-shell --verbose 2>&1 | while read line; do echo "$(date): $line"; done >> /var/log/bind-shell.log

# Monitor connections
watch -n 1 'netstat -an | grep 4444'

# Log connections only
bind-shell --verbose 2>&1 | grep "Connection from"
```

### Performance Best Practices

#### Resource Management

**1. Connection Limits**

Adjust based on expected load:
```bash
# Low traffic (1-5 concurrent users)
bind-shell --max-connections 5

# Medium traffic (5-20 concurrent users)
bind-shell --max-connections 20

# High traffic (20-50 concurrent users)
bind-shell --max-connections 50
```

**2. System Resources**

Monitor resource usage:
```bash
# CPU and memory
top -p $(pgrep -f bind-shell)

# Network connections
ss -tnp | grep bind-shell

# File descriptors
lsof -p $(pgrep -f bind-shell)
```

Set resource limits (systemd):
```ini
[Service]
MemoryLimit=512M
CPUQuota=50%
LimitNOFILE=1024
```

**3. Network Optimization**

```bash
# Use localhost for local connections (faster)
bind-shell --host 127.0.0.1
```

Optimize buffer sizes in code:
```python
# Default is 4096, adjust if needed
BUFFER_SIZE = 8192  # For large outputs
BUFFER_SIZE = 2048  # For small outputs
```

#### Scalability

**1. Horizontal Scaling**

Run multiple instances:
```bash
# Instance 1
bind-shell --host 127.0.0.1 --port 4444 &

# Instance 2
bind-shell --host 127.0.0.1 --port 4445 &

# Instance 3
bind-shell --host 127.0.0.1 --port 4446 &
```

Load balancing:
```bash
# Use HAProxy or nginx
# Round-robin to multiple bind-shell instances
```

**2. Vertical Scaling**

```bash
# System-wide limits
sudo sysctl -w net.core.somaxconn=1024
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=2048

# Application limits
bind-shell --max-connections 100
```

### Operational Best Practices

#### Deployment

**1. Environment Separation**

```bash
# Development: Local only, verbose logging
bind-shell --host 127.0.0.1 --port 4444 --verbose

# Testing: Isolated network, moderate logging
bind-shell --host 10.0.1.100 --port 4444

# Production: Restricted access, minimal logging
bind-shell --host 127.0.0.1 --port 4444
```

**2. Configuration Management**

Use environment variables:
```bash
# .env file
BIND_SHELL_HOST=127.0.0.1
BIND_SHELL_PORT=4444
BIND_SHELL_MAX_CONN=20

# Load and use
source .env
bind-shell --host $BIND_SHELL_HOST --port $BIND_SHELL_PORT
```

Use configuration files:
```bash
# config.sh
#!/bin/bash
HOST="127.0.0.1"
PORT="4444"
MAX_CONN="20"

bind-shell --host $HOST --port $PORT --max-connections $MAX_CONN
```

**3. Process Management**

Use systemd:
```ini
[Unit]
Description=Bind Shell Server
After=network.target

[Service]
Type=simple
User=bindshell
ExecStart=/usr/local/bin/bind-shell --host 127.0.0.1 --port 4444
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Use supervisord:
```ini
[program:bind-shell]
command=bind-shell --host 127.0.0.1 --port 4444
autostart=true
autorestart=true
stderr_logfile=/var/log/bind-shell.err.log
stdout_logfile=/var/log/bind-shell.out.log
```

#### Monitoring

**1. Health Checks**

Simple check:
```bash
#!/bin/bash
nc -zv localhost 4444 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Server is running"
else
    echo "Server is down"
    systemctl restart bind-shell
fi
```

Advanced check:
```python
import socket

def health_check(host, port):
    try:
        sock = socket.socket()
        sock.settimeout(5)
        sock.connect((host, port))
        sock.recv(1024)  # Welcome message
        sock.close()
        return True
    except:
        return False

if not health_check("localhost", 4444):
    print("Server unhealthy")
```

**2. Metrics Collection**

Log analysis:
```bash
# Count connections
grep "Connection from" /var/log/bind-shell.log | wc -l

# Find most active IPs
grep "Connection from" /var/log/bind-shell.log | awk '{print $NF}' | sort | uniq -c | sort -rn
```

Prometheus metrics (custom):
```python
from prometheus_client import Counter, Gauge

connections_total = Counter('bindshell_connections_total', 'Total connections')
active_connections = Gauge('bindshell_active_connections', 'Active connections')
```

#### Backup and Recovery

**1. Configuration Backup**

```bash
# Backup configuration
tar -czf bind-shell-config-$(date +%Y%m%d).tar.gz \
    /etc/systemd/system/bind-shell.service \
    /etc/bind-shell/

# Restore configuration
tar -xzf bind-shell-config-20240101.tar.gz -C /
```

**2. Disaster Recovery**

```bash
# 1. Stop service
sudo systemctl stop bind-shell

# 2. Reinstall package
pip install --force-reinstall bind-shell

# 3. Restore configuration
tar -xzf backup.tar.gz

# 4. Start service
sudo systemctl start bind-shell

# 5. Verify
nc -zv localhost 4444
```

### Testing Best Practices

**Unit Testing**

```python
import pytest
from simple_bind_shell import BindShell

def test_initialization():
    shell = BindShell(host="127.0.0.1", port=5555)
    assert shell.host == "127.0.0.1"
    assert shell.port == 5555

def test_command_execution():
    shell = BindShell()
    result = shell.run_command("echo test")
    assert b"test" in result
```

**Integration Testing**

```bash
#!/bin/bash
# Start server
bind-shell --host 127.0.0.1 --port 4444 &
SERVER_PID=$!
sleep 2

# Test connection
echo "whoami" | nc localhost 4444 > /tmp/test_output

# Verify output
if grep -q "$USER" /tmp/test_output; then
    echo "Test passed"
else
    echo "Test failed"
fi

# Cleanup
kill $SERVER_PID
```

**Load Testing**

```python
import socket
import threading
import time

def connect_client(host, port, duration):
    start = time.time()
    while time.time() - start < duration:
        try:
            sock = socket.socket()
            sock.connect((host, port))
            sock.sendall(b"echo test\n")
            sock.recv(1024)
            sock.close()
        except:
            pass

# Simulate 10 concurrent clients for 60 seconds
threads = []
for i in range(10):
    t = threading.Thread(target=connect_client, args=("localhost", 4444, 60))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

### Documentation Best Practices

**Code Documentation**

```python
from simple_bind_shell import BindShell

# Always document your usage
"""
Bind Shell Server Configuration

Purpose: Development testing server
Environment: Local development
Security: Localhost only, no external access
"""

shell = BindShell(
    host="127.0.0.1",  # Localhost only
    port=4444,          # Standard port
    max_connections=10  # Limit concurrent connections
)
```

**Operational Documentation**

Create runbook:
```markdown
# Bind Shell Runbook

## Starting Server
bind-shell --host 127.0.0.1 --port 4444

## Stopping Server
Ctrl+C or kill <PID>

## Troubleshooting
- Port in use: Change port or kill existing process
- Permission denied: Use port > 1024
- Connection refused: Check firewall rules

## Emergency Contacts
- Admin: admin@example.com
- On-call: +1-555-0100
```

### Compliance Best Practices

**Audit Trail**

```bash
# Log all commands executed
bind-shell --verbose 2>&1 | tee -a /var/log/bind-shell-audit.log

# Include timestamps
bind-shell --verbose 2>&1 | while read line; do 
    echo "$(date -Iseconds) $line" >> /var/log/bind-shell-audit.log
done
```

**Access Control**

```bash
# Restrict who can run bind-shell
sudo chown root:bindshell /usr/local/bin/bind-shell
sudo chmod 750 /usr/local/bin/bind-shell

# Add users to group
sudo usermod -aG bindshell username
```

**Data Protection**

```bash
# Ensure logs are protected
sudo chmod 600 /var/log/bind-shell.log
sudo chown bindshell:bindshell /var/log/bind-shell.log

# Rotate logs
# /etc/logrotate.d/bind-shell
/var/log/bind-shell.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 600 bindshell bindshell
}
```

## Security Considerations

### ⚠️ Critical Warnings

- **No Authentication**: Anyone who can connect can execute commands
- **No Encryption**: All traffic is plaintext (credentials, commands, output)
- **Full System Access**: Commands run with server process privileges
- **No Audit Trail**: Limited logging of executed commands (enable --verbose)

### Recommended Use Cases

✅ **Appropriate Uses:**
- Local development and testing
- Isolated lab environments
- CTF challenges and security training
- Penetration testing (authorized)
- Educational purposes

❌ **Inappropriate Uses:**
- Production systems
- Public-facing servers
- Systems with sensitive data
- Multi-tenant environments
- Compliance-regulated systems

### Secure Alternatives

For production use, consider:
- **SSH**: Encrypted, authenticated remote access
- **Ansible**: Automated configuration management
- **Fabric**: Python-based deployment tool
- **Paramiko**: Python SSH implementation

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/bind-shell.git
cd bind-shell

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=simple_bind_shell --cov-report=html

# Run specific test class
pytest tests/test_bind_shell.py::TestCommandExecution

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/

# Lint code
ruff check src/ tests/

# Fix linting issues
ruff check --fix src/ tests/
```

### Using Makefile

```bash
# Show available commands
make help

# Install dependencies
make install

# Run tests
make test

# Format and lint
make format
make lint

# Build package
make build

# Clean artifacts
make clean
```

### Building Distribution

```bash
# Build wheel and source distribution
python -m build

# Output in dist/
ls dist/
# bind_shell-0.1.0-py3-none-any.whl
# bind-shell-0.1.0.tar.gz
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Error: [Errno 98] Address already in use

# Solution 1: Use different port
bind-shell --port 5555

# Solution 2: Kill existing process
lsof -ti:4444 | xargs kill -9  # Linux/macOS
netstat -ano | findstr :4444   # Windows (find PID, then taskkill)
```

#### Permission Denied

```bash
# Error: [Errno 13] Permission denied

# Solution: Use non-privileged port (>1024)
bind-shell --port 4444  # Instead of port 80
```

#### Connection Refused

```bash
# Client can't connect

# Check server is running
netstat -tuln | grep 4444  # Linux/macOS
netstat -an | findstr 4444 # Windows

# Check firewall
sudo ufw status  # Linux

# Try localhost
nc 127.0.0.1 4444
```

#### Command Timeout

```bash
# Long-running commands timeout after 30s

# Solution: Break into smaller commands or modify timeout in code
# Edit src/simple_bind_shell/bind_shell.py
# Change: timeout=30 to timeout=300
```

### Debug Mode

```bash
# Enable verbose logging
bind-shell --verbose

# Redirect to file
bind-shell --verbose 2>&1 | tee debug.log

# Python logging
export PYTHONVERBOSE=1
bind-shell
```

### Getting Help

```bash
# Show help
bind-shell --help

# Check version
bind-shell --version

# View documentation
cat docs/BEST_PRACTICES.md
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `pytest`
5. Format code: `black src/ tests/`
6. Commit: `git commit -m "Add feature"`
7. Push: `git push origin feature-name`
8. Create Pull Request

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided for educational and testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. The authors assume no liability for misuse or damage caused by this software.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bind-shell/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bind-shell/discussions)
- **Security**: See [SECURITY.md](SECURITY.md)

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Tested with [pytest](https://pytest.org/)
- Formatted with [Black](https://black.readthedocs.io/)
- Linted with [Ruff](https://github.com/astral-sh/ruff)
