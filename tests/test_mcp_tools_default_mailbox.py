"""Tests for MCP tools using default_mailbox configuration."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_email_server.app import (
    delete_emails,
    download_attachment,
    get_emails_content,
    list_emails_metadata,
)
from mcp_email_server.config import EmailServer, EmailSettings
from mcp_email_server.emails.models import (
    AttachmentDownloadResponse,
    EmailBodyResponse,
    EmailContentBatchResponse,
    EmailMetadata,
    EmailMetadataPageResponse,
)


class TestMcpToolsDefaultMailbox:
    """Test MCP tools respect the default_mailbox configuration."""

    @pytest.mark.asyncio
    async def test_list_emails_metadata_uses_default_mailbox(self):
        """Test list_emails_metadata uses handler's default_mailbox when mailbox is None."""
        now = datetime.now(timezone.utc)
        email_metadata = EmailMetadata(
            email_id="12345",
            subject="Test Subject",
            sender="sender@example.com",
            recipients=["recipient@example.com"],
            date=now,
            attachments=[],
        )

        email_metadata_page = EmailMetadataPageResponse(
            page=1,
            page_size=10,
            before=None,
            since=None,
            subject=None,
            emails=[email_metadata],
            total=1,
        )

        # Mock handler with custom default_mailbox
        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "INBOX.Work"
        mock_handler.get_emails_metadata.return_value = email_metadata_page

        with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
            result = await list_emails_metadata(
                account_name="test_account",
            )

            assert result == email_metadata_page
            # Verify that default_mailbox was used
            mock_handler.get_emails_metadata.assert_called_once_with(
                page=1,
                page_size=10,
                before=None,
                since=None,
                subject=None,
                from_address=None,
                to_address=None,
                order="desc",
                mailbox="INBOX.Work",
            )

    @pytest.mark.asyncio
    async def test_list_emails_metadata_explicit_mailbox_overrides_default(self):
        """Test that explicit mailbox parameter overrides default_mailbox."""
        now = datetime.now(timezone.utc)
        email_metadata = EmailMetadata(
            email_id="12345",
            subject="Test Subject",
            sender="sender@example.com",
            recipients=["recipient@example.com"],
            date=now,
            attachments=[],
        )

        email_metadata_page = EmailMetadataPageResponse(
            page=1,
            page_size=10,
            before=None,
            since=None,
            subject=None,
            emails=[email_metadata],
            total=1,
        )

        # Mock handler with custom default_mailbox
        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "INBOX.Work"
        mock_handler.get_emails_metadata.return_value = email_metadata_page

        with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
            result = await list_emails_metadata(
                account_name="test_account",
                mailbox="Sent",
            )

            assert result == email_metadata_page
            # Verify that explicit mailbox was used, not default
            mock_handler.get_emails_metadata.assert_called_once_with(
                page=1,
                page_size=10,
                before=None,
                since=None,
                subject=None,
                from_address=None,
                to_address=None,
                order="desc",
                mailbox="Sent",
            )

    @pytest.mark.asyncio
    async def test_get_emails_content_uses_default_mailbox(self):
        """Test get_emails_content uses handler's default_mailbox when mailbox is None."""
        now = datetime.now(timezone.utc)
        email_body = EmailBodyResponse(
            email_id="12345",
            subject="Test Subject",
            sender="sender@example.com",
            recipients=["recipient@example.com"],
            date=now,
            body="Test body content",
            attachments=[],
        )

        batch_response = EmailContentBatchResponse(
            emails=[email_body],
            requested_count=1,
            retrieved_count=1,
            failed_ids=[],
        )

        # Mock handler with custom default_mailbox
        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "Archive"
        mock_handler.get_emails_content.return_value = batch_response

        with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
            result = await get_emails_content(
                account_name="test_account",
                email_ids=["12345"],
            )

            assert result == batch_response
            # Verify that default_mailbox was used
            mock_handler.get_emails_content.assert_called_once_with(["12345"], "Archive")

    @pytest.mark.asyncio
    async def test_get_emails_content_explicit_mailbox_overrides_default(self):
        """Test that explicit mailbox parameter overrides default_mailbox."""
        now = datetime.now(timezone.utc)
        email_body = EmailBodyResponse(
            email_id="12345",
            subject="Test Subject",
            sender="sender@example.com",
            recipients=["recipient@example.com"],
            date=now,
            body="Test body content",
            attachments=[],
        )

        batch_response = EmailContentBatchResponse(
            emails=[email_body],
            requested_count=1,
            retrieved_count=1,
            failed_ids=[],
        )

        # Mock handler with custom default_mailbox
        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "Archive"
        mock_handler.get_emails_content.return_value = batch_response

        with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
            result = await get_emails_content(
                account_name="test_account",
                email_ids=["12345"],
                mailbox="Drafts",
            )

            assert result == batch_response
            # Verify that explicit mailbox was used, not default
            mock_handler.get_emails_content.assert_called_once_with(["12345"], "Drafts")

    @pytest.mark.asyncio
    async def test_delete_emails_uses_default_mailbox(self):
        """Test delete_emails uses handler's default_mailbox when mailbox is None."""
        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "Trash"
        mock_handler.delete_emails.return_value = (["12345"], [])

        with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
            result = await delete_emails(
                account_name="test_account",
                email_ids=["12345"],
            )

            assert result == "Successfully deleted 1 email(s)"
            # Verify that default_mailbox was used
            mock_handler.delete_emails.assert_called_once_with(["12345"], "Trash")

    @pytest.mark.asyncio
    async def test_delete_emails_explicit_mailbox_overrides_default(self):
        """Test that explicit mailbox parameter overrides default_mailbox."""
        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "Trash"
        mock_handler.delete_emails.return_value = (["12345"], [])

        with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
            result = await delete_emails(
                account_name="test_account",
                email_ids=["12345"],
                mailbox="Spam",
            )

            assert result == "Successfully deleted 1 email(s)"
            # Verify that explicit mailbox was used, not default
            mock_handler.delete_emails.assert_called_once_with(["12345"], "Spam")

    @pytest.mark.asyncio
    async def test_download_attachment_uses_default_mailbox(self):
        """Test download_attachment uses handler's default_mailbox when mailbox is None."""
        attachment_response = AttachmentDownloadResponse(
            email_id="12345",
            attachment_name="document.pdf",
            mime_type="application/pdf",
            size=1024,
            saved_path="/tmp/document.pdf",
        )

        mock_settings = MagicMock()
        mock_settings.enable_attachment_download = True

        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "INBOX.Attachments"
        mock_handler.download_attachment.return_value = attachment_response

        with patch("mcp_email_server.app.get_settings", return_value=mock_settings):
            with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
                result = await download_attachment(
                    account_name="test_account",
                    email_id="12345",
                    attachment_name="document.pdf",
                    save_path="/tmp/document.pdf",
                )

                assert result == attachment_response
                # Verify that default_mailbox was used
                mock_handler.download_attachment.assert_called_once_with(
                    "12345", "document.pdf", "/tmp/document.pdf", "INBOX.Attachments"
                )

    @pytest.mark.asyncio
    async def test_download_attachment_explicit_mailbox_overrides_default(self):
        """Test that explicit mailbox parameter overrides default_mailbox."""
        attachment_response = AttachmentDownloadResponse(
            email_id="12345",
            attachment_name="document.pdf",
            mime_type="application/pdf",
            size=1024,
            saved_path="/tmp/document.pdf",
        )

        mock_settings = MagicMock()
        mock_settings.enable_attachment_download = True

        mock_handler = AsyncMock()
        mock_handler.default_mailbox = "INBOX.Attachments"
        mock_handler.download_attachment.return_value = attachment_response

        with patch("mcp_email_server.app.get_settings", return_value=mock_settings):
            with patch("mcp_email_server.app.dispatch_handler", return_value=mock_handler):
                result = await download_attachment(
                    account_name="test_account",
                    email_id="12345",
                    attachment_name="document.pdf",
                    save_path="/tmp/document.pdf",
                    mailbox="Archive",
                )

                assert result == attachment_response
                # Verify that explicit mailbox was used, not default
                mock_handler.download_attachment.assert_called_once_with(
                    "12345", "document.pdf", "/tmp/document.pdf", "Archive"
                )
