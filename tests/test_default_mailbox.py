"""Tests for default_mailbox configuration feature."""

import os

import pytest

from mcp_email_server.config import EmailSettings, Settings


class TestDefaultMailboxConfig:
    """Test default_mailbox configuration through environment variables and settings."""

    def test_email_settings_default_mailbox_default_value(self, monkeypatch):
        """Test that default_mailbox defaults to INBOX when not specified."""
        monkeypatch.setenv("MCP_EMAIL_SERVER_EMAIL_ADDRESS", "test@example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_PASSWORD", "pass123")
        monkeypatch.setenv("MCP_EMAIL_SERVER_IMAP_HOST", "imap.example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_SMTP_HOST", "smtp.example.com")

        result = EmailSettings.from_env()
        assert result is not None
        assert result.default_mailbox == "INBOX"

    def test_email_settings_default_mailbox_custom_value(self, monkeypatch):
        """Test that default_mailbox can be set via environment variable."""
        monkeypatch.setenv("MCP_EMAIL_SERVER_EMAIL_ADDRESS", "test@example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_PASSWORD", "pass123")
        monkeypatch.setenv("MCP_EMAIL_SERVER_IMAP_HOST", "imap.example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_SMTP_HOST", "smtp.example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_DEFAULT_MAILBOX", "INBOX.Work")

        result = EmailSettings.from_env()
        assert result is not None
        assert result.default_mailbox == "INBOX.Work"

    def test_email_settings_default_mailbox_various_folders(self, monkeypatch):
        """Test default_mailbox with various folder names."""
        base_env = {
            "MCP_EMAIL_SERVER_EMAIL_ADDRESS": "test@example.com",
            "MCP_EMAIL_SERVER_PASSWORD": "pass123",
            "MCP_EMAIL_SERVER_IMAP_HOST": "imap.example.com",
            "MCP_EMAIL_SERVER_SMTP_HOST": "smtp.example.com",
        }

        test_cases = [
            "Sent",
            "Archive",
            "INBOX.Archive",
            "[Gmail]/All Mail",
            "Drafts",
            "INBOX/Important",
        ]

        for folder in test_cases:
            # Clear previous environment variables
            for key in list(os.environ.keys()):
                if key.startswith("MCP_EMAIL_SERVER_"):
                    monkeypatch.delenv(key, raising=False)

            # Set base environment
            for key, value in base_env.items():
                monkeypatch.setenv(key, value)

            # Set custom mailbox
            monkeypatch.setenv("MCP_EMAIL_SERVER_DEFAULT_MAILBOX", folder)

            result = EmailSettings.from_env()
            assert result is not None
            assert result.default_mailbox == folder, f"Failed for folder: {folder}"

    def test_settings_with_default_mailbox_from_env(self, monkeypatch, tmp_path):
        """Test Settings initialization with default_mailbox from environment."""
        config_file = tmp_path / "empty.toml"
        config_file.write_text("")
        monkeypatch.setenv("MCP_EMAIL_SERVER_CONFIG_PATH", str(config_file))

        monkeypatch.setenv("MCP_EMAIL_SERVER_EMAIL_ADDRESS", "work@example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_PASSWORD", "workpass")
        monkeypatch.setenv("MCP_EMAIL_SERVER_IMAP_HOST", "imap.work.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_SMTP_HOST", "smtp.work.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_ACCOUNT_NAME", "work")
        monkeypatch.setenv("MCP_EMAIL_SERVER_DEFAULT_MAILBOX", "INBOX.Work")

        settings = Settings()
        assert len(settings.emails) == 1
        assert settings.emails[0].account_name == "work"
        assert settings.emails[0].default_mailbox == "INBOX.Work"

    def test_email_settings_init_with_default_mailbox(self):
        """Test EmailSettings.init() with default_mailbox parameter."""
        email = EmailSettings.init(
            account_name="test",
            full_name="Test User",
            email_address="test@example.com",
            user_name="test@example.com",
            password="pass123",
            imap_host="imap.example.com",
            smtp_host="smtp.example.com",
            default_mailbox="Archive",
        )

        assert email.default_mailbox == "Archive"

    def test_email_settings_toml_with_default_mailbox(self, monkeypatch, tmp_path):
        """Test that default_mailbox can be stored and loaded from TOML config."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("""
[[emails]]
account_name = "test"
full_name = "Test User"
email_address = "test@example.com"
default_mailbox = "INBOX.Custom"
created_at = "2025-01-01T00:00:00+00:00"
updated_at = "2025-01-01T00:00:00+00:00"

[emails.incoming]
user_name = "test"
password = "pass"
host = "imap.test.com"
port = 993
use_ssl = true

[emails.outgoing]
user_name = "test"
password = "pass"
host = "smtp.test.com"
port = 465
use_ssl = true
""")

        monkeypatch.setenv("MCP_EMAIL_SERVER_CONFIG_PATH", str(config_file))

        settings = Settings()
        assert len(settings.emails) == 1
        assert settings.emails[0].default_mailbox == "INBOX.Custom"

    def test_email_settings_default_mailbox_override_from_env(self, monkeypatch, tmp_path):
        """Test that environment variable overrides TOML config for default_mailbox."""
        config_file = tmp_path / "config.toml"
        config_file.write_text("""
[[emails]]
account_name = "test"
full_name = "Test User"
email_address = "test@example.com"
default_mailbox = "INBOX.FromToml"
created_at = "2025-01-01T00:00:00+00:00"
updated_at = "2025-01-01T00:00:00+00:00"

[emails.incoming]
user_name = "test"
password = "pass"
host = "imap.test.com"
port = 993
use_ssl = true

[emails.outgoing]
user_name = "test"
password = "pass"
host = "smtp.test.com"
port = 465
use_ssl = true
""")

        monkeypatch.setenv("MCP_EMAIL_SERVER_CONFIG_PATH", str(config_file))
        monkeypatch.setenv("MCP_EMAIL_SERVER_ACCOUNT_NAME", "test")
        monkeypatch.setenv("MCP_EMAIL_SERVER_EMAIL_ADDRESS", "test@example.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_PASSWORD", "pass")
        monkeypatch.setenv("MCP_EMAIL_SERVER_IMAP_HOST", "imap.test.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_SMTP_HOST", "smtp.test.com")
        monkeypatch.setenv("MCP_EMAIL_SERVER_DEFAULT_MAILBOX", "INBOX.FromEnv")

        settings = Settings()
        assert len(settings.emails) == 1
        assert settings.emails[0].default_mailbox == "INBOX.FromEnv"
