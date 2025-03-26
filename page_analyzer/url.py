"""Validation module for URL"""
from urllib.parse import urlparse
import validators


def validate_url(url):
    """Validates URL"""
    if not validators.url(url):
        return False, "Некорректный URL"
    if len(url) > 255:
        return False, "URL превышает 255 символов"
    return True, None


def normalize_url(url):
    """Get hostname from URL"""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"
