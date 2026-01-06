"""
NET_SCAN - Web Crawler
Advanced site crawling with JavaScript rendering, form detection, and input identification
"""

import asyncio
from typing import Set, List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse, parse_qs
import logging
from datetime import datetime

from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

class CrawledPage:
    """Represents a crawled page with extracted data"""
    
    def __init__(self, url: str, method: str = "GET"):
        self.url = url
        self.method = method
        self.html = ""
        self.status_code = 0
        self.headers: Dict[str, str] = {}
        self.forms: List[Dict] = []
        self.inputs: List[Dict] = []
        self.links: List[str] = []
        self.parameters: List[str] = []
        self.crawled_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "url": self.url,
            "method": self.method,
            "status": self.status_code,
            "forms_count": len(self.forms),
            "inputs_count": len(self.inputs),
            "links_count": len(self.links),
            "parameters": self.parameters,
            "crawled_at": self.crawled_at.isoformat()
        }

class WebCrawler:
    """Advanced web crawler with JavaScript rendering and form detection"""
    
    def __init__(
        self,
        start_url: str,
        max_depth: int = 3,
        max_pages: int = 100,
        timeout: int = 30,
        headless: bool = True,
        use_js_rendering: bool = True,
    ):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.timeout = timeout
        self.headless = headless
        self.use_js_rendering = use_js_rendering
        
        self.base_domain = urlparse(start_url).netloc
        self.crawled_urls: Set[str] = set()
        self.to_crawl: List[Tuple[str, int]] = [(start_url, 0)]
        self.pages: List[CrawledPage] = []
        self.browser: Optional[Browser] = None
        self.excluded_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.exe', '.iso',
            '.mp4', '.mp3', '.css', '.js', '.woff', '.woff2', '.ttf'
        }
    
    async def crawl(self) -> List[CrawledPage]:
        """Start crawling"""
        logger.info(f"Starting crawl of {self.start_url}")
        
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=self.headless)
            
            while self.to_crawl and len(self.crawled_urls) < self.max_pages:
                url, depth = self.to_crawl.pop(0)
                
                # Skip if already crawled or out of depth
                if url in self.crawled_urls or depth > self.max_depth:
                    continue
                
                # Skip external URLs
                if not self._is_same_domain(url):
                    continue
                
                # Skip binary files
                if self._has_excluded_extension(url):
                    continue
                
                logger.debug(f"Crawling {url} (depth: {depth})")
                page_data = await self._crawl_page(url)
                
                if page_data:
                    self.pages.append(page_data)
                    self.crawled_urls.add(url)
                    
                    # Add discovered links to queue
                    for link in page_data.links:
                        if link not in self.crawled_urls:
                            self.to_crawl.append((link, depth + 1))
                    
                    # Brief delay between requests
                    await asyncio.sleep(0.5)
            
            await self.browser.close()
        
        logger.info(f"Crawl complete. Discovered {len(self.pages)} pages")
        return self.pages
    
    async def _crawl_page(self, url: str) -> Optional[CrawledPage]:
        """Crawl a single page"""
        try:
            page_data = CrawledPage(url)
            
            if self.use_js_rendering:
                html = await self._render_with_js(url)
            else:
                html = await self._fetch_html(url)
            
            if not html:
                return None
            
            page_data.html = html
            
            # Parse page
            soup = BeautifulSoup(html, 'lxml')
            
            # Extract forms
            page_data.forms = self._extract_forms(soup, url)
            
            # Extract all input fields
            page_data.inputs = self._extract_inputs(soup, url)
            
            # Extract links
            page_data.links = self._extract_links(soup, url)
            
            # Extract query parameters
            parsed = urlparse(url)
            page_data.parameters = list(parse_qs(parsed.query).keys())
            
            return page_data
        
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return None
    
    async def _render_with_js(self, url: str) -> Optional[str]:
        """Render page with JavaScript using Playwright"""
        try:
            if not self.browser:
                return None
            
            page = await self.browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=self.timeout * 1000)
            
            # Wait for dynamic content
            await asyncio.sleep(1)
            
            html = await page.content()
            await page.close()
            
            return html
        
        except Exception as e:
            logger.debug(f"JS rendering failed for {url}: {e}")
            return None
    
    async def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML without JavaScript"""
        try:
            import aiohttp
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, ssl=False) as resp:
                    if resp.status == 200:
                        return await resp.text(errors='ignore')
        
        except Exception as e:
            logger.debug(f"HTML fetch failed for {url}: {e}")
        
        return None
    
    def _extract_forms(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract forms from HTML"""
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'action': urljoin(base_url, form.get('action', '')),
                'method': form.get('method', 'GET').upper(),
                'name': form.get('name', ''),
                'id': form.get('id', ''),
                'fields': []
            }
            
            # Extract form fields
            for input_field in form.find_all(['input', 'textarea', 'select']):
                field = {
                    'name': input_field.get('name', ''),
                    'type': input_field.get('type', 'text'),
                    'value': input_field.get('value', ''),
                }
                if field['name']:
                    form_data['fields'].append(field)
            
            forms.append(form_data)
        
        return forms
    
    def _extract_inputs(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all input fields"""
        inputs = []
        
        for input_field in soup.find_all(['input', 'textarea', 'select']):
            if input_field.get('name'):
                inputs.append({
                    'name': input_field.get('name'),
                    'type': input_field.get('type', 'text'),
                    'value': input_field.get('value', ''),
                    'id': input_field.get('id', ''),
                })
        
        return inputs
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract links from HTML"""
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href and not href.startswith('#'):
                full_url = urljoin(base_url, href)
                
                # Remove fragments
                full_url = full_url.split('#')[0]
                
                if full_url and self._is_same_domain(full_url):
                    links.append(full_url)
        
        return list(set(links))  # Remove duplicates
    
    def _is_same_domain(self, url: str) -> bool:
        """Check if URL is from same domain"""
        try:
            domain = urlparse(url).netloc
            return domain == self.base_domain
        except:
            return False
    
    def _has_excluded_extension(self, url: str) -> bool:
        """Check if URL has excluded file extension"""
        for ext in self.excluded_extensions:
            if url.lower().endswith(ext):
                return True
        return False
    
    def get_all_parameters(self) -> Set[str]:
        """Get all testable parameters"""
        params = set()
        
        for page in self.pages:
            params.update(page.parameters)
            for input_field in page.inputs:
                if input_field.get('name'):
                    params.add(input_field['name'])
            for form in page.forms:
                for field in form.get('fields', []):
                    if field.get('name'):
                        params.add(field['name'])
        
        return params
    
    def get_testable_endpoints(self) -> List[Dict]:
        """Get all testable endpoints (forms + URL params)"""
        endpoints = []
        
        # URL parameters
        for page in self.pages:
            if page.parameters:
                endpoints.append({
                    'url': page.url,
                    'method': 'GET',
                    'parameters': page.parameters,
                    'type': 'url_param'
                })
        
        # Forms
        for page in self.pages:
            for form in page.forms:
                endpoints.append({
                    'url': form['action'],
                    'method': form['method'],
                    'parameters': [f['name'] for f in form.get('fields', [])],
                    'type': 'form'
                })
        
        return endpoints
