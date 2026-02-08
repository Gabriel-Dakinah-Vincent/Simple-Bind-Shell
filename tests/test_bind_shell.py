"""Tests for bind shell functionality."""

import pytest
from simple_bind_shell import BindShell


def test_bind_shell_initialization():
    """Test BindShell initialization with default parameters."""
    shell = BindShell()
    assert shell.host == "0.0.0.0"
    assert shell.port == 4444
    assert shell.max_connections == 4


def test_bind_shell_custom_parameters():
    """Test BindShell initialization with custom parameters."""
    shell = BindShell(host="127.0.0.1", port=5555, max_connections=10)
    assert shell.host == "127.0.0.1"
    assert shell.port == 5555
    assert shell.max_connections == 10


def test_run_command():
    """Test command execution."""
    shell = BindShell()
    result = shell.run_command("echo test")
    assert b"test" in result
