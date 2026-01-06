"""
NET_SCAN - XSS Detector
Cross-Site Scripting vulnerability detection
"""

import re
from typing import List, Dict, Optional
import logging
from net_scan.utils.payloads import PayloadGenerator
from net_scan.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)

class XSSDetector:
    """Detect Cross-Site Scripting vulnerabilities"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.findings: List[Dict] = []
    
    async def test_url_parameter(
        self,
        url: str,
        param: str,
        method: str = "GET"
    ) -> List[Dict]:
        """Test URL parameter for XSS"""
        findings = []
        
        logger.debug(f"Testing {method} {url}?{param}=<payload> for XSS")
        
        # Reflected XSS
        reflected = await self._test_reflected_xss(url, param, method)
        if reflected:
            findings.extend(reflected)
        
        return findings
    
    async def _test_reflected_xss(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Test for reflected XSS"""
        findings = []
        payloads = PayloadGenerator.get_xss_payloads(5)
        
        for payload in payloads:
            try:
                response = await self._send_payload(url, param, payload, method)
                
                if response and self._is_payload_reflected(response, payload):
                    # Verify it's executable
                    if self._is_executable(payload, response):
                        findings.append({
                            'type': 'Cross-Site Scripting (XSS)',
                            'severity': 'HIGH',
                            'url': url,
                            'parameter': param,
                            'method': method,
                            'payload': payload,
                            'evidence': 'Payload reflected in response without encoding',
                            'cvss_score': 7.5,
                        })
                        break
            
            except Exception as e:
                logger.debug(f"XSS test error: {e}")
        
        return findings
    
    async def _send_payload(
        self,
        url: str,
        param: str,
        payload: str,
        method: str
    ) -> Optional[Dict]:
        """Send XSS payload"""
        try:
            if method == "GET":
                sep = '&' if '?' in url else '?'
                test_url = f"{url}{sep}{param}={payload}"
                return await self.http_client.get(test_url)
            else:
                data = {param: payload}
                return await self.http_client.post(url, data=data)
        except Exception as e:
            logger.debug(f"Payload send error: {e}")
            return None
    
    def _is_payload_reflected(self, response: Dict, payload: str) -> bool:
        """Check if payload is reflected in response"""
        content = response.get('content', '')
        
        # Check for exact payload
        if payload in content:
            return True
        
        # Check for URL-encoded versions
        import urllib.parse
        encoded = urllib.parse.quote(payload)
        if encoded in content:
            return True
        
        return False
    
    def _is_executable(self, payload: str, response: Dict) -> bool:
        """Check if payload would be executable in browser"""
        content = response.get('content', '')
        
        # Check if it's in an executable context (not in comments or strings)
        dangerous_contexts = [
            (r'<script[^>]*>' + re.escape(payload), 'inside script tag'),
            (r'on\w+\s*=\s*["\']?' + re.escape(payload), 'in event handler'),
            (r'href\s*=\s*["\']javascript:' + re.escape(payload), 'in href'),
        ]
        
        for pattern, context in dangerous_contexts:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
