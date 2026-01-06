"""
NET_SCAN - HTTP Client with security best practices
Async HTTP handling with connection pooling, timeouts, and retry logic
"""

import asyncio
import hashlib
from typing import Dict, Optional, Any, List
from urllib.parse import urljoin, urlparse
import aiohttp
import httpx
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    """Secure HTTP client with connection pooling and retry logic"""
    
    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        proxy: Optional[str] = None,
        user_agent: str = "NET_SCAN/1.0 (Security Scanner)"
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.proxy = proxy
        self.user_agent = user_agent
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache: Dict[str, tuple] = {}
        self.cache_ttl = 300  # 5 minutes
        self.rate_limit_delay = 0.5  # seconds between requests
        self.last_request_time = 0
    
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
            ttl_dns_cache=300,
            ssl=False  # For testing; use True in production with proper certs
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": self.user_agent}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = asyncio.get_event_loop().time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = asyncio.get_event_loop().time()
    
    def _get_cache_key(self, method: str, url: str, **kwargs) -> str:
        """Generate cache key"""
        key_data = f"{method}:{url}:{str(kwargs)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _check_cache(self, key: str) -> Optional[Any]:
        """Check if cached response is still valid"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return data
            else:
                del self.cache[key]
        return None
    
    async def get(
        self,
        url: str,
        **kwargs
    ) -> Optional[httpx.Response]:
        """GET request with retry logic and caching"""
        return await self._request("GET", url, **kwargs)
    
    async def post(
        self,
        url: str,
        data: Optional[Dict] = None,
        **kwargs
    ) -> Optional[httpx.Response]:
        """POST request"""
        return await self._request("POST", url, data=data, **kwargs)
    
    async def _request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Optional[httpx.Response]:
        """Internal request handler with retry logic"""
        
        if not self.session:
            raise RuntimeError("HTTPClient not initialized. Use async context manager.")
        
        # Check cache for GET requests
        if method == "GET":
            cache_key = self._get_cache_key(method, url, **kwargs)
            cached = self._check_cache(cache_key)
            if cached:
                logger.debug(f"Cache hit for {url}")
                return cached
        
        await self._rate_limit()
        
        for attempt in range(self.max_retries):
            try:
                async with self.session.request(
                    method,
                    url,
                    proxy=self.proxy,
                    ssl=False,
                    **kwargs
                ) as resp:
                    # Read response
                    response_data = {
                        'status': resp.status,
                        'headers': dict(resp.headers),
                        'content': await resp.text(errors='ignore'),
                        'url': str(resp.url),
                        'timestamp': datetime.now()
                    }
                    
                    # Cache successful responses
                    if method == "GET" and resp.status == 200:
                        cache_key = self._get_cache_key(method, url, **kwargs)
                        self.cache[cache_key] = (response_data, datetime.now())
                    
                    return response_data
            
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on {method} {url} (attempt {attempt + 1})")
                if attempt == self.max_retries - 1:
                    return None
                await asyncio.sleep(2 ** attempt)
            
            except aiohttp.ClientConnectorError as e:
                logger.warning(f"Connection error for {url}: {e}")
                if attempt == self.max_retries - 1:
                    return None
                await asyncio.sleep(2 ** attempt)
            
            except Exception as e:
                logger.error(f"Unexpected error in request: {e}", exc_info=True)
                return None
        
        return None
    
    async def head(self, url: str, **kwargs) -> Optional[Dict]:
        """HEAD request"""
        await self._rate_limit()
        try:
            async with self.session.head(url, proxy=self.proxy, ssl=False, **kwargs) as resp:
                return {
                    'status': resp.status,
                    'headers': dict(resp.headers),
                    'url': str(resp.url)
                }
        except Exception as e:
            logger.error(f"HEAD request failed for {url}: {e}")
            return None

class SyncHTTPClient:
    """Synchronous HTTP client wrapper using httpx"""
    
    def __init__(
        self,
        timeout: int = 30,
        proxy: Optional[str] = None,
        user_agent: str = "NET_SCAN/1.0 (Security Scanner)"
    ):
        self.timeout = timeout
        self.proxy = proxy
        self.user_agent = user_agent
        self.client = httpx.Client(
            timeout=timeout,
            proxies=proxy,
            headers={"User-Agent": user_agent},
            verify=False  # For testing; use True in production
        )
    
    def get(self, url: str, **kwargs) -> Optional[httpx.Response]:
        """GET request"""
        try:
            return self.client.get(url, **kwargs)
        except Exception as e:
            logger.error(f"GET request failed for {url}: {e}")
            return None
    
    def post(self, url: str, data: Optional[Dict] = None, **kwargs) -> Optional[httpx.Response]:
        """POST request"""
        try:
            return self.client.post(url, data=data, **kwargs)
        except Exception as e:
            logger.error(f"POST request failed for {url}: {e}")
            return None
    
    def close(self):
        """Close client"""
        self.client.close()
