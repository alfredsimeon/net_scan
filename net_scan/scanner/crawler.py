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
        
        try:
            async with async_playwright() as p:
                try:
                    self.browser = await p.chromium.launch(headless=self.headless)
                except Exception as e:
                    logger.warning(f"JavaScript rendering unavailable: {e}")
                    logger.info("Falling back to static HTML parsing (no JS rendering)")
                    self.use_js_rendering = False
                    self.browser = None
                
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
                
                if self.browser:
                    await self.browser.close()
        
        except Exception as e:
            logger.error(f"Crawling error: {e}")
        
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
            
            try:
                # Wait for network to settle
                await page.goto(url, wait_until="networkidle", timeout=self.timeout * 1000)
            except:
                # If networkidle times out, still try to get content
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout * 1000)
                except:
                    pass
            
            # Wait for dynamic content and additional resources to load
            await asyncio.sleep(2)
            
            # Try to wait for common framework loaders
            try:
                await page.wait_for_load_state("networkidle", timeout=3000)
            except:
                pass
            
            # Scroll to trigger lazy loading and additional rendering
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
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
        """Extract forms from HTML including JavaScript-rendered forms"""
        forms = []
        
        # Extract traditional HTML forms
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
            
            if form_data['action'] or form_data['fields']:  # Only add if has action or fields
                forms.append(form_data)
        
        # Extract API endpoints from script tags (common in SPAs)
        api_endpoints = self._extract_api_endpoints(soup, base_url)
        
        # Convert API endpoints to form-like structures for testing
        for endpoint in api_endpoints:
            forms.append({
                'action': endpoint['url'],
                'method': endpoint['method'],
                'name': endpoint.get('name', ''),
                'id': '',
                'fields': endpoint.get('params', [])
            })
        
        return forms
    
    def _extract_api_endpoints(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract API endpoints from script tags and HTML attributes"""
        endpoints = []
        
        # Extract from fetch/axios calls in script tags
        for script in soup.find_all('script'):
            if script.string:
                script_content = script.string.lower()
                
                # Look for common API patterns
                api_patterns = [
                    r'fetch\(["\'](/api/[^"\']+)["\']',
                    r'axios\.(?:get|post|put|delete)\(["\'](/api/[^"\']+)["\']',
                    r'\.get\(["\'](/api/[^"\']+)["\']',
                    r'\.post\(["\'](/api/[^"\']+)["\']',
                    r'url\s*:\s*["\'](/api/[^"\']+)["\']',
                ]
                
                for pattern in api_patterns:
                    matches = re.findall(pattern, script_content)
                    for match in matches:
                        full_url = urljoin(base_url, match)
                        if self._is_same_domain(full_url):
                            endpoints.append({
                                'url': full_url,
                                'method': 'POST',  # Most API endpoints accept POST
                                'name': match.split('/')[-1],
                                'params': []
                            })
        
        # Extract from common input attributes (data-api, data-endpoint)
        for elem in soup.find_all(attrs={'data-api': True}):
            api_url = elem.get('data-api')
            if api_url:
                full_url = urljoin(base_url, api_url)
                if self._is_same_domain(full_url):
                    endpoints.append({
                        'url': full_url,
                        'method': 'POST',
                        'name': 'api_endpoint',
                        'params': []
                    })
        
        return endpoints
    
    def _extract_inputs(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all input fields from forms and standalone elements"""
        inputs = []
        seen = set()
        
        # From form inputs
        for input_field in soup.find_all(['input', 'textarea', 'select']):
            name = input_field.get('name')
            if name and name not in seen:
                inputs.append({
                    'name': name,
                    'type': input_field.get('type', 'text'),
                    'value': input_field.get('value', ''),
                    'id': input_field.get('id', ''),
                })
                seen.add(name)
        
        # Extract from data attributes (common in React/Vue apps)
        for elem in soup.find_all(attrs={"data-testid": True}):
            name = elem.get('data-testid')
            if name and name not in seen and 'input' in name.lower():
                inputs.append({
                    'name': name,
                    'type': 'text',
                    'value': '',
                    'id': elem.get('id', ''),
                })
                seen.add(name)
        
        # Extract placeholders that suggest input fields
        for elem in soup.find_all(placeholder=True):
            placeholder = elem.get('placeholder', '').lower()
            # Look for common input field hints
            if any(hint in placeholder for hint in ['email', 'username', 'password', 'search', 'query', 'name']):
                name = elem.get('name') or placeholder.replace(' ', '_')
                if name and name not in seen:
                    inputs.append({
                        'name': name,
                        'type': 'text',
                        'value': '',
                        'id': elem.get('id', ''),
                    })
                    seen.add(name)
        
        return inputs
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Aggressively extract all possible links from HTML"""
        links = []
        
        # Standard links
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href and not href.startswith('#'):
                full_url = urljoin(base_url, href)
                full_url = full_url.split('#')[0]  # Remove fragments
                if full_url and self._is_same_domain(full_url):
                    links.append(full_url)
        
        # Links from onclick attributes
        for elem in soup.find_all(onclick=True):
            onclick = elem.get('onclick', '')
            if 'http' in onclick or '/' in onclick:
                urls = re.findall(r"['\"](/[^'\"]+)['\"]|['\"]([a-z]+://[^'\"]+)['\"]", onclick)
                for match in urls:
                    url = match[0] or match[1]
                    if url:
                        full_url = urljoin(base_url, url)
                        if self._is_same_domain(full_url):
                            links.append(full_url)
        
        # Links from data attributes
        for elem in soup.find_all(attrs={'data-url': True}):
            data_url = elem.get('data-url')
            if data_url:
                full_url = urljoin(base_url, data_url)
                if self._is_same_domain(full_url):
                    links.append(full_url)
        
        # Links from href attributes in any element
        for elem in soup.find_all(href=True):
            href = elem.get('href', '')
            if href and href.startswith('/'):
                full_url = urljoin(base_url, href)
                if self._is_same_domain(full_url):
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
        """Get all testable endpoints - forms, URL params, paths, and common endpoints"""
        endpoints = []
        
        # 1. Extract URL parameters from discovered pages
        for page in self.pages:
            if page.parameters:
                endpoints.append({
                    'url': page.url,
                    'method': 'GET',
                    'parameters': page.parameters,
                    'type': 'url_param'
                })
        
        # 2. Extract form endpoints
        for page in self.pages:
            for form in page.forms:
                params = [f['name'] for f in form.get('fields', []) if f.get('name')]
                if params:  # Only if form has fields
                    endpoints.append({
                        'url': form['action'],
                        'method': form['method'],
                        'parameters': params,
                        'type': 'form'
                    })
        
        # 3. Inject common test parameters into discovered URLs (advanced testing)
        common_params = ['id', 'search', 'query', 'q', 'name', 'user', 'file', 'path', 'category', 'product', 'page', 'sort', 'filter', 'email', 'username']
        for page in self.pages:
            # Only add if no parameters already found on this URL
            if not page.parameters:
                for param in common_params[:5]:  # Limit to 5 to avoid explosion
                    endpoints.append({
                        'url': page.url,
                        'method': 'GET',
                        'parameters': [param],
                        'type': 'injected_param'
                    })
        
        # 4. Add endpoints for direct path traversal testing on each discovered URL
        for page in self.pages:
            if page.url:
                endpoints.append({
                    'url': page.url,
                    'method': 'GET',
                    'parameters': [],  # Will test path itself
                    'type': 'path_test'
                })
        
        # 5. Add common admin/sensitive endpoints (if not already discovered)
        base_url = self.start_url.rsplit('/', 1)[0]
        common_endpoints = [
            '/admin', '/api', '/api/v1', '/api/admin', '/search', '/download',
            '/upload', '/login', '/config', '/status', '/health', '/debug'
        ]
        for endpoint_path in common_endpoints:
            test_url = urljoin(base_url, endpoint_path)
            if self._is_same_domain(test_url):
                endpoints.append({
                    'url': test_url,
                    'method': 'GET',
                    'parameters': [],
                    'type': 'common_endpoint'
                })
        
        return endpoints
