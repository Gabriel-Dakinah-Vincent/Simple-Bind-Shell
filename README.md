# Bind Shell

A lightweight bind shell implementation in Python with a CLI and a small, focused API.

[![CI](https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell/workflows/CI/badge.svg)](https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell/actions)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Table of Contents

- [Features](#features)
- [Security Warning](#security-warning)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration Reference](#configuration-reference)
- [Usage: CLI](#usage-cli)
- [Usage: Python API](#usage-python-api)
- [Client Examples](#client-examples)
- [Advanced Usage](#advanced-usage)
- [Manual Test Checklist](#manual-test-checklist)
- [Architecture](#architecture)
- [Best Practices](#best-practices)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## Features

- Multi-threaded connection handling
- Command execution with a per-command timeout
- Client idle timeout
- Configurable host, port, and backlog size
- CLI and Python API
- Cross-platform (Windows, Linux, macOS)

## Security Warning

This bind shell provides unauthenticated, unencrypted command execution.
Do not expose it to untrusted networks or production systems.
Use it only in controlled environments (local dev, lab, CTF, or authorized testing).

## Installation

### Prerequisites

- Python 3.8+
- pip

Optional but recommended:
- Git (for source installs)
- A virtual environment (venv)

### From PyPI (Recommended)

```bash
pip install bind-shell
```

Verify:

```bash
bind-shell --version
```

### From Source

```bash
git clone https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell.git
cd bind-shell
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install .
```

Verify:

```bash
bind-shell --help
```

### Development Installation

```bash
git clone https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell.git
cd bind-shell
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

This installs additional tools: pytest, black, ruff, coverage.

### Upgrade / Uninstall

```bash
# Upgrade
pip install -U bind-shell

# Uninstall
pip uninstall bind-shell
```

## Quick Start

### 1) Start the server

```bash
# Start with defaults (0.0.0.0:4444)
bind-shell
```

### 2) Connect from a client

```bash
# Linux/macOS
nc 127.0.0.1 4444

# Windows (if ncat is installed)
ncat 127.0.0.1 4444
```

### 3) Run commands

```text
whoami
pwd
exit
```

## Configuration Reference

### CLI options

- `--host`, `-h` (default: `0.0.0.0`)
- `--port`, `-p` (default: `4444`)
- `--max-connections`, `-m` (default: `4`)
- `--command-timeout` (default: `30` seconds)
- `--client-timeout` (default: `300` seconds)
- `--verbose` (enable debug logging)

### Environment variables

- `BIND_SHELL_HOST`
- `BIND_SHELL_PORT`
- `BIND_SHELL_MAX_CONN`
- `BIND_SHELL_COMMAND_TIMEOUT`
- `BIND_SHELL_CLIENT_TIMEOUT`

Note: `max-connections` controls the socket listen backlog (queued connections). It does not cap active threads.

## Usage: CLI

### CLI basics

1. Start the server:

```bash
bind-shell --host 127.0.0.1 --port 4444
```

2. Connect from a client (examples):

```bash
nc 127.0.0.1 4444
```

3. Stop the server with `Ctrl+C` in the server terminal.

### CLI help

```bash
bind-shell --help
bind-shell --version
```

### Local-only (safe default for testing)

```bash
bind-shell --host 127.0.0.1 --port 4444
```

### LAN testing (controlled environments only)

```bash
bind-shell --host 192.168.1.50 --port 4444
```

### Custom timeouts

```bash
# 60s command timeout, 10-minute client idle timeout
bind-shell --command-timeout 60 --client-timeout 600
```

### Backlog sizing

```bash
# Allow more queued connections
bind-shell --max-connections 50
```

### Verbose logging

```bash
bind-shell --verbose
bind-shell --verbose 2>&1 | tee server.log
```

### Run in background (examples)

Linux/macOS:

```bash
nohup bind-shell --host 127.0.0.1 --port 4444 > bind-shell.log 2>&1 &
```

Windows PowerShell:

```powershell
Start-Process -NoNewWindow -FilePath "bind-shell" -ArgumentList "--host 127.0.0.1 --port 4444"
```

## Usage: Python API

### Blocking server

```python
from simple_bind_shell import BindShell

shell = BindShell()
shell.start()
```

### Custom configuration

```python
from simple_bind_shell import BindShell

shell = BindShell(
    host="127.0.0.1",
    port=5555,
    max_connections=10,
    command_timeout=60,
    client_timeout=600,
)

shell.start()
```

### Non-blocking server

```python
import threading
import time
from simple_bind_shell import BindShell

shell = BindShell(host="127.0.0.1", port=4444)
thread = threading.Thread(target=shell.start, daemon=True)
thread.start()

# Do other work
time.sleep(10)

# Stop the server
shell.stop()
```

### Error handling

```python
from simple_bind_shell import BindShell, BindShellError

try:
    shell = BindShell(host="0.0.0.0", port=80)
    shell.start()
except BindShellError as exc:
    print(f"Failed to start server: {exc}")
```

### Run a single command

```python
from simple_bind_shell import BindShell

shell = BindShell()
result = shell.run_command("echo Hello World")
print(result.decode(errors="replace"))
```

## Client Examples

### Netcat (Linux/macOS)

```bash
nc 127.0.0.1 4444
```

### Ncat (Windows)

```cmd
ncat 127.0.0.1 4444
```

### Telnet

```bash
telnet 127.0.0.1 4444
```

### PowerShell client (no extra tools)

```powershell
$client = New-Object System.Net.Sockets.TcpClient("127.0.0.1",4444)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$writer.AutoFlush = $true
$reader = New-Object System.IO.StreamReader($stream)

$writer.WriteLine("whoami")
$reader.ReadLine()

$writer.WriteLine("pwd")
$reader.ReadLine()

$writer.WriteLine("exit")
$client.Close()
```

### Python client

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 4444))

client.sendall(b"whoami\n")
print(client.recv(4096).decode(errors="replace"))

client.sendall(b"exit\n")
client.close()
```

## Advanced Usage

### Running as a systemd service (Linux)

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

### Docker container

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

### Environment variables

```bash
# Set defaults via environment
export BIND_SHELL_HOST=127.0.0.1
export BIND_SHELL_PORT=5555

# Use in script
bind-shell --host $BIND_SHELL_HOST --port $BIND_SHELL_PORT
```

### Process management

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

### Windows Task Scheduler (auto-start on boot)

Use Task Scheduler to start the server automatically after reboot. This is intended for authorized, controlled environments only.

PowerShell (run as Administrator):

```powershell
# Replace with your Python path if bind-shell isn't on the system PATH
$python = "C:\Python310\python.exe"
$args = "-m simple_bind_shell.cli --host 127.0.0.1 --port 4444"

# Create a task that runs at startup
schtasks /Create /TN "BindShell" /SC ONSTART /RL HIGHEST `
    /TR "`"$python`" $args"

# Check task status
schtasks /Query /TN "BindShell" /V /FO LIST
```

To stop or remove:

```powershell
schtasks /End /TN "BindShell"
schtasks /Delete /TN "BindShell" /F
```

Tip: For a user-scoped task instead of a system task, add `/RU "$env:USERNAME"` and omit `/RL HIGHEST`.

## Manual Test Checklist

1. Start server: `bind-shell --host 127.0.0.1 --port 4444 --verbose`
2. Connect using `nc`, `ncat`, or the PowerShell client above
3. Run commands: `whoami`, `pwd`, `echo test`
4. Confirm output returns
5. Run `exit` and confirm the client disconnects
6. Confirm server continues to accept new connections

## Architecture

### Package Structure

```
bind-shell/
|-- src/simple_bind_shell/    # Source code (src-layout)
|   |-- __init__.py            # Package initialization and public API
|   |-- version.py             # Version management
|   |-- bind/                  # Bind shell implementation
|   |   |-- __init__.py        # Bind package exports
|   |   `-- bind_shell.py      # Core bind shell logic
|   `-- cli.py                 # Command-line interface
|-- tests/                     # Test suite
`-- pyproject.toml             # Project metadata and dependencies
```

### Protocol (text-based)

1. Client connects
2. Client sends a command ending with a newline
3. Server executes the command and returns stdout/stderr
4. Client sends `exit` to close the session

## Best Practices

### Security Best Practices

#### Restrict network access

```bash
# Always bind to localhost for local testing
bind-shell --host 127.0.0.1

# Avoid on production systems
# bind-shell --host 0.0.0.0
```

Use firewall rules (Linux):

```bash
# iptables
sudo iptables -A INPUT -p tcp --dport 4444 -s 192.168.1.100 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 4444 -j DROP

# ufw
sudo ufw allow from 192.168.1.100 to any port 4444
sudo ufw deny 4444
```

Network segmentation example:

```bash
bind-shell --host 10.0.1.100 --port 4444
```

#### Use non-privileged ports

```bash
# Good: Ports > 1024
bind-shell --port 4444
bind-shell --port 8080
bind-shell --port 9999

# Bad: Privileged ports (require root)
# bind-shell --port 80
# bind-shell --port 443
```

#### Implement access controls

```bash
# Create dedicated user without login shell
sudo useradd -r -s /bin/false bindshell

# Run as dedicated user
sudo -u bindshell bind-shell --host 127.0.0.1
```

SELinux / AppArmor examples:

```bash
# SELinux
sudo semanage port -a -t bindshell_port_t -p tcp 4444

# AppArmor
sudo aa-enforce /etc/apparmor.d/usr.local.bin.bind-shell
```

### Application Security

#### Input validation

The CLI validates inputs automatically:

```bash
# Port validation (1-65535)
bind-shell --port 70000  # Will fail

# Connection limits (1-100)
bind-shell --max-connections 200  # Will fail
```

#### Command execution safety

Avoid dangerous commands in client sessions:

```bash
# Dangerous - avoid these:
rm -rf /
dd if=/dev/zero of=/dev/sda
:(){ :|:& };:  # Fork bomb
```

Timeout defaults:

- Command timeout: 30 seconds
- Connection timeout: 5 minutes

#### Logging and monitoring

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

#### Connection limits

```bash
# Low traffic (1-5 concurrent users)
bind-shell --max-connections 5

# Medium traffic (5-20 concurrent users)
bind-shell --max-connections 20

# High traffic (20-50 concurrent users)
bind-shell --max-connections 50
```

#### System resources

```bash
# CPU and memory
top -p $(pgrep -f bind-shell)

# Network connections
ss -tnp | grep bind-shell

# File descriptors
lsof -p $(pgrep -f bind-shell)
```

Resource limits (systemd example):

```ini
[Service]
MemoryLimit=512M
CPUQuota=50%
LimitNOFILE=1024
```

#### Network optimization

```bash
# Use localhost for local connections (faster)
bind-shell --host 127.0.0.1
```

Buffer size is defined in `src/simple_bind_shell/bind/bind_shell.py` as `BUFFER_SIZE` (default 2048).
Adjust with care if you expect very large output per command.

### Scalability

#### Horizontal scaling

```bash
# Instance 1
bind-shell --host 127.0.0.1 --port 4444 &

# Instance 2
bind-shell --host 127.0.0.1 --port 4445 &

# Instance 3
bind-shell --host 127.0.0.1 --port 4446 &
```

Load balancing example:

Use HAProxy or nginx for round-robin distribution.

#### Vertical scaling

```bash
# System-wide limits
sudo sysctl -w net.core.somaxconn=1024
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=2048

# Application limits
bind-shell --max-connections 100
```

### Operational Best Practices

#### Deployment profiles

```bash
# Development: Local only, verbose logging
bind-shell --host 127.0.0.1 --port 4444 --verbose

# Testing: Isolated network, moderate logging
bind-shell --host 10.0.1.100 --port 4444

# Production: Restricted access, minimal logging
bind-shell --host 127.0.0.1 --port 4444
```

#### Configuration management

Environment variables:

```bash
# .env file
BIND_SHELL_HOST=127.0.0.1
BIND_SHELL_PORT=4444
BIND_SHELL_MAX_CONN=20
```

Shell config example:

```bash
# config.sh
HOST="127.0.0.1"
PORT="4444"
MAX_CONN="20"

bind-shell --host $HOST --port $PORT --max-connections $MAX_CONN
```

#### Process management

Systemd:

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

Supervisord:

```ini
[program:bind-shell]
command=bind-shell --host 127.0.0.1 --port 4444
autostart=true
autorestart=true
stderr_logfile=/var/log/bind-shell.err.log
stdout_logfile=/var/log/bind-shell.out.log
```

### Monitoring

#### Health checks

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
        sock.recv(1024)
        sock.close()
        return True
    except Exception:
        return False

if not health_check("localhost", 4444):
    print("Server unhealthy")
```

#### Metrics collection (custom)

```bash
# Count connections
grep "Connection from" /var/log/bind-shell.log | wc -l

# Find most active IPs
grep "Connection from" /var/log/bind-shell.log | awk '{print $NF}' | sort | uniq -c | sort -rn
```

Prometheus example (custom instrumentation required):

```python
from prometheus_client import Counter, Gauge

connections_total = Counter('bindshell_connections_total', 'Total connections')
active_connections = Gauge('bindshell_active_connections', 'Active connections')
```

### Backup and Recovery

#### Configuration backup

```bash
# Backup configuration
tar -czf bind-shell-config-$(date +%Y%m%d).tar.gz \
    /etc/systemd/system/bind-shell.service \
    /etc/bind-shell/
```

#### Disaster recovery

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

#### Unit testing

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

#### Integration testing

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

#### Load testing

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
        except Exception:
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

#### Code documentation

```python
from simple_bind_shell import BindShell

"""
Bind Shell Server Configuration

Purpose: Development testing server
Environment: Local development
Security: Localhost only, no external access
"""

shell = BindShell(
    host="127.0.0.1",
    port=4444,
    max_connections=10,
)
```

#### Operational documentation

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

#### Audit trail

```bash
# Log all commands executed (not enabled by default)
bind-shell --verbose 2>&1 | tee -a /var/log/bind-shell-audit.log

# Include timestamps
bind-shell --verbose 2>&1 | while read line; do
    echo "$(date -Iseconds) $line" >> /var/log/bind-shell-audit.log
done
```

#### Access control

```bash
# Restrict who can run bind-shell
sudo chown root:bindshell /usr/local/bin/bind-shell
sudo chmod 750 /usr/local/bin/bind-shell

# Add users to group
sudo usermod -aG bindshell username
```

#### Data protection

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

### Critical warnings

- No authentication: Anyone who can connect can execute commands.
- No encryption: All traffic is plaintext.
- Full system access: Commands run with server process privileges.
- No command audit by default: Verbose logging does not log commands.

### Recommended use cases

- Local development and testing
- Isolated lab environments
- CTF challenges and security training
- Authorized penetration testing
- Educational purposes

### Inappropriate use cases

- Production systems
- Public-facing servers
- Systems with sensitive data
- Multi-tenant environments
- Compliance-regulated systems

### Secure alternatives

- SSH (encrypted, authenticated remote access)
- Ansible (automation and orchestration)
- Fabric (Python-based deployment tool)
- Paramiko (Python SSH implementation)

## Troubleshooting

### Port already in use

```bash
# Choose a different port
bind-shell --port 5555

# Find and kill the process (Windows)
netstat -ano | findstr :4444
```

### Permission denied (Linux/macOS)

```bash
# Use a port > 1024
bind-shell --port 4444
```

### Connection refused

```bash
# Check server is running
netstat -an | findstr 4444   # Windows
netstat -tuln | grep 4444    # Linux/macOS
```

### Command timeout

```bash
# Increase timeout to 120 seconds
bind-shell --command-timeout 120
```

## Development

### Setup

```bash
git clone https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell.git
cd bind-shell
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

### Tests

```bash
pytest -v
```

### TestPyPI install and verification

Step-by-step:

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

2. Install from TestPyPI:

```bash
pip install -i https://test.pypi.org/simple/ bind-shell
```

3. Verify the CLI:

```bash
bind-shell --version
bind-shell --help
```

4. Run a quick end-to-end check (Linux/macOS):

```bash
bind-shell --host 127.0.0.1 --port 4444 --verbose
```

In a new terminal:

```bash
printf "whoami\nexit\n" | nc 127.0.0.1 4444
```

5. Run a quick end-to-end check (Windows PowerShell):

```powershell
bind-shell --host 127.0.0.1 --port 4444 --verbose
```

In a new PowerShell window:

```powershell
$client = New-Object System.Net.Sockets.TcpClient("127.0.0.1",4444)
$stream = $client.GetStream()
$writer = New-Object System.IO.StreamWriter($stream)
$writer.AutoFlush = $true
$reader = New-Object System.IO.StreamReader($stream)

$writer.WriteLine("whoami")
$reader.ReadLine()

$writer.WriteLine("exit")
$client.Close()
```

6. Optional cleanup:

```bash
pip uninstall bind-shell
```

### Lint and format

```bash
black src/ tests/
ruff check src/ tests/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided for educational and testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. The authors assume no liability for misuse or damage caused by this software.

## Support

- Issues: [GitHub Issues](https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell/issues)
- Discussions: [GitHub Discussions](https://github.com/Gabriel-Dakinah-Vincent/Simple-Bind-Shell/discussions)
- Security: See [SECURITY.md](SECURITY.md)

## Acknowledgments

- Built with Click for CLI
- Tested with pytest
- Formatted with Black
- Linted with Ruff
