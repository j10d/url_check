"""URL checking functionality."""

import requests
from urllib.parse import urlparse


def check_url(url: str, timeout: int = 5, use_browser_agent: bool = False) -> tuple[bool, str]:
    """
    Check if a URL exists and is accessible.

    Args:
        url: The URL to check
        timeout: Request timeout in seconds (default: 5)
        use_browser_agent: If True, use a browser-like User-Agent header to avoid
                          bot detection (default: False)

    Returns:
        A tuple of (result, explanation) where:
        - result is True if the URL is accessible, False otherwise
        - explanation describes the outcome or reason for failure
    """
    # Validate URL format
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            return False, "Invalid URL: Missing protocol (http:// or https://)"
        if not parsed.netloc:
            return False, "Invalid URL: Malformed URL format"
        if parsed.scheme not in ['http', 'https']:
            return False, f"Invalid URL: Unsupported protocol '{parsed.scheme}'"
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"

    # Prepare headers
    headers = {}
    if use_browser_agent:
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    # Attempt to make the request
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True, headers=headers)

        # Check if there were redirects
        if response.history:
            final_url = response.url
            return True, f"Redirects to {final_url}"

        # Check status code
        if response.status_code == 404:
            return False, "404 Not Found"
        elif 400 <= response.status_code < 600:
            return False, f"HTTP {response.status_code} error"
        else:
            return True, "URL is accessible"

    except requests.exceptions.Timeout:
        return False, "Connection timeout: Request took too long to respond"

    except requests.exceptions.ConnectionError as e:
        error_msg = str(e).lower()
        if "nodename nor servname provided" in error_msg or "name or service not known" in error_msg or "getaddrinfo failed" in error_msg:
            return False, "DNS resolution failed: Unable to resolve domain name"
        elif "connection refused" in error_msg:
            return False, "Connection refused: Server is not accepting connections"
        else:
            return False, f"Network connection error: Unable to connect to server"

    except requests.exceptions.TooManyRedirects:
        return False, "Too many redirects"

    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}"

    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
