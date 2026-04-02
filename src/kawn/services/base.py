from ..client import KawnClient, AsyncKawnClient


class BaseService:
    """Base synchronous service."""

    def __init__(self, client: KawnClient):
        if not isinstance(client, KawnClient):
            raise TypeError("Expected a MisrajClient instance.")
        self._client = client


class AsyncBaseService:
    """Base asynchronous service."""

    def __init__(self, client: AsyncKawnClient):
        if not isinstance(client, AsyncKawnClient):
            raise TypeError("Expected a AsyncMisrajClient instance.")
        self._client = client
