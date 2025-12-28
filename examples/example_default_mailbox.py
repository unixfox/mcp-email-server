#!/usr/bin/env python3
"""
Example: Configuring Default IMAP Folder via Environment Variable

This example demonstrates how to use the MCP_EMAIL_SERVER_DEFAULT_MAILBOX
environment variable to set a custom default IMAP folder for email operations.

Usage:
    # Use INBOX (default)
    python example_default_mailbox.py
    
    # Use a custom folder
    MCP_EMAIL_SERVER_DEFAULT_MAILBOX="INBOX.Work" python example_default_mailbox.py
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_email_server.config import EmailSettings


def demonstrate_default_mailbox():
    """Demonstrate the default_mailbox configuration."""
    
    # Set up minimal environment variables for EmailSettings.from_env()
    os.environ.setdefault("MCP_EMAIL_SERVER_EMAIL_ADDRESS", "example@example.com")
    os.environ.setdefault("MCP_EMAIL_SERVER_PASSWORD", "example_password")
    os.environ.setdefault("MCP_EMAIL_SERVER_IMAP_HOST", "imap.example.com")
    os.environ.setdefault("MCP_EMAIL_SERVER_SMTP_HOST", "smtp.example.com")
    
    # Get the default mailbox from environment or use default
    custom_mailbox = os.environ.get("MCP_EMAIL_SERVER_DEFAULT_MAILBOX")
    
    print("=" * 60)
    print("Default IMAP Folder Configuration Example")
    print("=" * 60)
    print()
    
    if custom_mailbox:
        print(f"✓ Custom default mailbox configured: {custom_mailbox}")
    else:
        print("✓ Using default mailbox: INBOX")
    
    print()
    print("Creating EmailSettings from environment variables...")
    
    # Create EmailSettings from environment
    email_settings = EmailSettings.from_env()
    
    if email_settings:
        print(f"✓ EmailSettings created successfully")
        print(f"  Account name: {email_settings.account_name}")
        print(f"  Email address: {email_settings.email_address}")
        print(f"  Default mailbox: {email_settings.default_mailbox}")
        print()
        print("Usage in MCP tools:")
        print("  - list_emails_metadata() will use:", email_settings.default_mailbox)
        print("  - get_emails_content() will use:", email_settings.default_mailbox)
        print("  - delete_emails() will use:", email_settings.default_mailbox)
        print("  - download_attachment() will use:", email_settings.default_mailbox)
        print()
        print("Note: You can still override by passing explicit mailbox parameter")
    else:
        print("✗ Failed to create EmailSettings from environment")
    
    print()
    print("Configuration via TOML file:")
    print("  Add 'default_mailbox = \"INBOX.Work\"' to your email account config")
    print()
    print("Configuration via environment variable:")
    print("  Set MCP_EMAIL_SERVER_DEFAULT_MAILBOX=\"INBOX.Work\"")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_default_mailbox()
