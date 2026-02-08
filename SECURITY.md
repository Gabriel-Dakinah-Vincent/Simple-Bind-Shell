# Security Policy

## Security Considerations

This package implements a bind shell, which by design allows remote command execution. Please be aware of the following security implications:

### Warnings

- **No Authentication**: This implementation does not include authentication mechanisms
- **No Encryption**: All communication is transmitted in plaintext
- **Command Execution**: Allows arbitrary command execution on the host system
- **Network Exposure**: Binding to 0.0.0.0 exposes the service to all network interfaces

### Recommended Usage

- Use only in controlled, isolated environments (e.g., testing, CTF challenges)
- Never expose to untrusted networks or the public internet
- Consider using SSH or other secure alternatives for production use
- Run with minimal privileges (non-root user)
- Use firewall rules to restrict access

### Reporting Security Issues

If you discover a security vulnerability, please email security@example.com with details.

## Disclaimer

This software is provided for educational and testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.
