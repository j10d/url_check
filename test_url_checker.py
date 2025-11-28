"""Tests for URL checking functionality."""

import pytest
from url_checker import check_url


class TestURLChecker:
    """Test cases for the check_url function."""

    def test_valid_url_returns_true(self):
        """Test that a valid, accessible URL returns True."""
        result, explanation = check_url("https://www.google.com")
        assert result is True
        assert isinstance(explanation, str)

    def test_404_not_found_returns_false(self):
        """Test that a 404 Not Found returns False with explanation."""
        result, explanation = check_url("https://www.google.com/this-page-does-not-exist-404")
        assert result is False
        assert "404" in explanation or "not found" in explanation.lower()

    def test_invalid_url_format_returns_false(self):
        """Test that an invalid URL format returns False with explanation."""
        result, explanation = check_url("not-a-valid-url")
        assert result is False
        assert "invalid" in explanation.lower() or "malformed" in explanation.lower()

    def test_missing_protocol_returns_false(self):
        """Test that a URL without protocol returns False with explanation."""
        result, explanation = check_url("www.google.com")
        assert result is False
        assert "invalid" in explanation.lower() or "protocol" in explanation.lower()

    def test_connection_timeout_returns_false(self):
        """Test that a connection timeout returns False with explanation."""
        # Using a non-routable IP address to trigger timeout
        result, explanation = check_url("http://10.255.255.1")
        assert result is False
        assert "timeout" in explanation.lower() or "connect" in explanation.lower()

    def test_network_error_dns_failure(self):
        """Test that a DNS failure returns False with explanation."""
        result, explanation = check_url("https://this-domain-does-not-exist-12345.com")
        assert result is False
        assert any(keyword in explanation.lower() for keyword in ["dns", "resolve", "network", "connection"])

    def test_redirect_returns_true_with_target_url(self):
        """Test that a redirect returns True with the target URL in explanation."""
        # Azure redirects to localized version
        result, explanation = check_url("https://azure.microsoft.com/")
        assert result is True
        assert "redirect" in explanation.lower() or "https://azure.microsoft.com/" in explanation.lower()
        # The explanation should contain the target URL
        assert "http" in explanation  # Should contain a URL

    def test_redirect_http_to_https(self):
        """Test that HTTP to HTTPS redirect is handled correctly."""
        result, explanation = check_url("http://github.com")
        assert result is True
        # Should mention redirect or show the https URL
        assert "redirect" in explanation.lower() or "https://github.com" in explanation.lower()

    def test_connection_refused_returns_false(self):
        """Test that a connection refused error returns False with explanation."""
        # Using localhost on a port that's likely not in use
        result, explanation = check_url("http://localhost:9999")
        assert result is False
        assert any(keyword in explanation.lower() for keyword in ["connection", "refused", "connect"])

    def test_bot_blocking_site_fails_without_browser_mode(self):
        """Test that a site blocking bots returns False without browser mode."""
        # Equinix.com blocks requests with bot User-Agents
        result, explanation = check_url("https://www.equinix.com")
        assert result is False
        assert "403" in explanation or "forbidden" in explanation.lower()

    def test_bot_blocking_site_succeeds_with_browser_mode(self):
        """Test that a site blocking bots returns True when using browser mode."""
        # Equinix.com blocks bots but allows browser-like User-Agents
        result, explanation = check_url("https://www.equinix.com", use_browser_agent=True)
        assert result is True
        assert isinstance(explanation, str)
