# url_check

A Python utility to check if a URL exists and is accessible. The function validates URL formats, handles redirects, and provides detailed explanations for both successful and failed requests.

## Features

- Validates URL format and protocol
- Checks if websites are accessible
- Detects and reports redirects with target URLs
- Optional browser mode to bypass bot detection
- Handles common error scenarios (404, timeouts, DNS failures, connection errors)
- Returns detailed explanations for all outcomes
- Built with test-driven development (TDD)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/j10d/url_check.git
cd url_check
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from url_checker import check_url

# Check a valid URL
result, explanation = check_url("https://www.google.com")
print(f"Result: {result}")          # True
print(f"Explanation: {explanation}") # "URL is accessible"

# Check a URL that redirects
result, explanation = check_url("https://azure.microsoft.com/")
print(f"Result: {result}")          # True
print(f"Explanation: {explanation}") # "Redirects to https://azure.microsoft.com/en-us"

# Check a non-existent page
result, explanation = check_url("https://www.google.com/nonexistent")
print(f"Result: {result}")          # False
print(f"Explanation: {explanation}") # "404 Not Found"

# Check an invalid URL
result, explanation = check_url("not-a-valid-url")
print(f"Result: {result}")          # False
print(f"Explanation: {explanation}") # "Invalid URL: Missing protocol (http:// or https://)"
```

### Function Signature

```python
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
```

### Custom Timeout

```python
# Set a custom timeout (in seconds)
result, explanation = check_url("https://example.com", timeout=10)
```

### Browser Mode (Bypass Bot Detection)

Some websites block requests from automated scripts by checking the User-Agent header. By default, `check_url` identifies itself as `python-requests`, which some sites reject with a 403 Forbidden error. You can enable browser mode to mimic a real browser:

```python
# Without browser mode (may be blocked)
result, explanation = check_url("https://www.equinix.com")
print(f"Result: {result}")          # False
print(f"Explanation: {explanation}") # "HTTP 403 error"

# With browser mode (appears as Chrome browser)
result, explanation = check_url("https://www.equinix.com", use_browser_agent=True)
print(f"Result: {result}")          # True
print(f"Explanation: {explanation}") # "URL is accessible" or "Redirects to..."
```

**When to use browser mode:**
- When checking websites that implement bot detection
- When you get 403 Forbidden errors despite the site working in your browser
- When you need to check if a site is accessible to real users

**When NOT to use browser mode:**
- When respecting robots.txt and bot identification is important
- When you want to be transparent about automated access
- For API endpoints (use appropriate authentication instead)

## Return Values

The function returns a tuple containing:
1. **Boolean result**: `True` if the URL is accessible, `False` otherwise
2. **String explanation**: Details about the outcome

### Success Cases (True)
- `"URL is accessible"` - Standard successful response
- `"Redirects to <target_url>"` - URL redirects to another location

### Failure Cases (False)
- `"404 Not Found"` - Page does not exist
- `"HTTP 403 error"` - Forbidden (often due to bot detection)
- `"Invalid URL: Missing protocol (http:// or https://)"` - URL missing scheme
- `"Invalid URL: Malformed URL format"` - Improperly formatted URL
- `"Connection timeout: Request took too long to respond"` - Request timed out
- `"DNS resolution failed: Unable to resolve domain name"` - DNS lookup failed
- `"Connection refused: Server is not accepting connections"` - Server rejected connection
- `"Network connection error: Unable to connect to server"` - General network error

## Running Tests

The project uses pytest for testing:

```bash
# Run all tests
pytest test_url_checker.py

# Run with verbose output
pytest test_url_checker.py -v
```

## Test Coverage

The test suite covers:
- Valid URLs
- 404 Not Found errors
- Invalid URL formats
- Missing protocols
- Connection timeouts
- DNS failures
- Redirects (HTTP to HTTPS, localized redirects)
- Connection refused errors
- Bot detection and browser mode functionality

## Requirements

- Python 3.7+
- requests >= 2.31.0
- pytest >= 7.0.0 (for testing)

## License

See LICENSE file for details.
