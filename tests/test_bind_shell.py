"""Tests for bind shell functionality."""

import pytest

from simple_bind_shell import BindShell, BindShellError


def test_bind_shell_initialization():
    """Test BindShell initialization with default parameters."""
    shell = BindShell()
    assert shell.host == "0.0.0.0"
    assert shell.port == 4444
    assert shell.max_connections == 4
    assert shell.command_timeout == 30
    assert shell.client_timeout == 300


def test_bind_shell_custom_parameters():
    """Test BindShell initialization with custom parameters."""
    shell = BindShell(
        host="127.0.0.1",
        port=5555,
        max_connections=10,
        command_timeout=10,
        client_timeout=120,
    )
    assert shell.host == "127.0.0.1"
    assert shell.port == 5555
    assert shell.max_connections == 10
    assert shell.command_timeout == 10
    assert shell.client_timeout == 120


@pytest.mark.parametrize(
    "kwargs",
    [
        {"port": 0},
        {"port": 70000},
        {"max_connections": 0},
        {"max_connections": 200},
        {"command_timeout": 0},
        {"client_timeout": 0},
    ],
)
def test_invalid_parameters(kwargs):
    """Test validation for invalid parameters."""
    with pytest.raises(BindShellError):
        BindShell(**kwargs)


def test_run_command():
    """Test command execution."""
    shell = BindShell()
    result = shell.run_command("echo test")
    assert b"test" in result
