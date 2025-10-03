"""Asynchronous CKMT API client"""

import os
import aiohttp
from typing import Optional, Dict, Any
from .exceptions import APIError, AuthenticationError, RateLimitError, NotFoundError, ValidationError


class AsyncCKMT:
    """
    Asynchronous client for the CKMT API.

    Example:
        >>> async with AsyncCKMT(api_key="your_api_key") as client:
        >>>     results = await client.search("nginx")
        >>>     host_info = await client.host("8.8.8.8")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize the async CKMT client.

        Args:
            api_key: API key for authentication. If not provided, will use CKMT_API_KEY env var.
            base_url: Base URL for the API. Defaults to CKMT_BASE_URL env var or https://api.ckmt.io
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.getenv("CKMT_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set CKMT_API_KEY or pass api_key parameter.")

        self.base_url = (base_url or os.getenv("CKMT_BASE_URL", "https://api.ckmt.io")).rstrip("/")
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "ckmt-sdk/1.0.0"
            },
            timeout=self.timeout
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def _ensure_session(self):
        """Ensure session is created."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "User-Agent": "ckmt-sdk/1.0.0"
                },
                timeout=self.timeout
            )

    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an async HTTP request to the API."""
        await self._ensure_session()
        url = f"{self.base_url}{endpoint}"

        try:
            async with self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers
            ) as response:
                text = await response.text()

                # Handle different status codes
                if response.status == 401:
                    raise AuthenticationError("Invalid API key", status_code=401, response=text)
                elif response.status == 404:
                    raise NotFoundError("Resource not found", status_code=404, response=text)
                elif response.status == 429:
                    raise RateLimitError("Rate limit exceeded", status_code=429, response=text)
                elif response.status == 422:
                    raise ValidationError("Validation error", status_code=422, response=text)
                elif response.status >= 400:
                    raise APIError(
                        f"API error: {text}",
                        status_code=response.status,
                        response=text
                    )

                return await response.json()

        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {str(e)}")

    async def search(
        self,
        query: Optional[str] = None,
        port: Optional[int] = None,
        service: Optional[str] = None,
        product: Optional[str] = None,
        version: Optional[str] = None,
        country: Optional[str] = None,
        asn: Optional[str] = None,
        os: Optional[str] = None,
        vuln: Optional[str] = None,
        http_title: Optional[str] = None,
        http_status: Optional[int] = None,
        technology: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        Search for hosts using various filters.

        Args:
            query: General search query
            port: Filter by port number
            service: Filter by service name
            product: Filter by product name
            version: Filter by version
            country: Filter by country code
            asn: Filter by ASN
            os: Filter by operating system
            vuln: Filter by vulnerability/CVE
            http_title: Filter by HTTP title
            http_status: Filter by HTTP status code
            technology: Filter by detected technology
            page: Page number (default: 1)
            size: Results per page (default: 10)

        Returns:
            Dictionary containing search results with total count, page info, and matches
        """
        params = {
            "query": query,
            "port": port,
            "service": service,
            "product": product,
            "version": version,
            "country": country,
            "asn": asn,
            "os": os,
            "vuln": vuln,
            "http_title": http_title,
            "http_status": http_status,
            "technology": technology,
            "page": page,
            "size": size
        }
        params = {k: v for k, v in params.items() if v is not None}

        return await self._request("GET", "/v1/search", params=params)

    async def host(self, ip: str) -> Dict[str, Any]:
        """Get all available information for a specific IP address."""
        return await self._request("GET", f"/v1/search/host/{ip}")

    async def count(
        self,
        query: Optional[str] = None,
        port: Optional[str] = None,
        country: Optional[str] = None
    ) -> Dict[str, Any]:
        """Count the number of hosts matching the search filters."""
        params = {
            "query": query,
            "port": port,
            "country": country
        }
        params = {k: v for k, v in params.items() if v is not None}

        return await self._request("GET", "/v1/search/count", params=params)

    async def facets(
        self,
        query: Optional[str] = None,
        facets: str = "country,port,service,technology"
    ) -> Dict[str, Any]:
        """Get aggregated facets for search results."""
        params = {
            "query": query,
            "facets": facets
        }
        params = {k: v for k, v in params.items() if v is not None}

        return await self._request("GET", "/v1/search/facets", params=params)

    async def ports(self, query: Optional[str] = None, size: int = 100) -> Dict[str, Any]:
        """Get a list of port numbers that have been used by hosts."""
        params = {"query": query, "size": size}
        params = {k: v for k, v in params.items() if v is not None}

        return await self._request("GET", "/v1/search/ports", params=params)

    async def services(self) -> Dict[str, Any]:
        """Get a list of all services that have been detected."""
        return await self._request("GET", "/v1/search/services")

    async def stats(self) -> Dict[str, Any]:
        """Get overall statistics about the indexed data."""
        return await self._request("GET", "/v1/search/stats")
