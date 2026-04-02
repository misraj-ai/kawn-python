class MisrajAPIError(Exception):
    """Base exception for all Misraj AI API errors."""
    pass


class AuthenticationError(MisrajAPIError):
    """Raised when the API key is invalid or missing."""
    pass


class RateLimitError(MisrajAPIError):
    """Raised when the API rate limit is exceeded."""
    pass


class InvalidRequestError(MisrajAPIError):
    """Raised when the request payload is malformed."""
    pass


class PollingTimeoutError(MisrajAPIError):
    """Raised when an asynchronous processing task times out."""
    pass


class ProcessingFailedError(MisrajAPIError):
    """Raised when a model fails to process a file (e.g., failed OCR status)."""
    pass


def handle_http_error(response):
    """Utility to map HTTP status codes to exceptions."""
    if response.status_code == 401:
        raise AuthenticationError("Invalid or missing API key.")
    elif response.status_code == 429:
        raise RateLimitError("Rate limit exceeded. Please slow down your requests.")
    elif 400 <= response.status_code < 500:
        raise InvalidRequestError(f"Client Error {response.status_code}: {response.text}")
    elif response.status_code >= 500:
        raise MisrajAPIError(f"Server Error {response.status_code}: {response.text}")
