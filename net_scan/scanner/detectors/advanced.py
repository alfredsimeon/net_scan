"""
NET_SCAN - Additional Detectors
Path traversal, XXE, SSRF, and other vulnerability detectors
"""

from typing import List, Dict, Optional
import logging
import re
from net_scan.utils.http_client import HTTPClient
from net_scan.utils.payloads import PayloadGenerator

logger = logging.getLogger(__name__)

class PathTraversalDetector:
    """Detect path traversal vulnerabilities"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
    
    async def test_url_parameter(
        self,
        url: str,
        param: str,
        method: str = "GET"
    ) -> List[Dict]:
        """Test for path traversal"""
        findings = []
        payloads = PayloadGenerator.get_path_traversal_payloads()
        
        for payload in payloads[:5]:
            try:
                response = await self._send_payload(url, param, payload, method)
                if response and self._has_file_disclosure(response):
                    findings.append({
                        'type': 'Path Traversal',
                        'severity': 'MEDIUM',
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': 'File/directory content disclosed',
                        'cvss_score': 7.5,
                    })
                    break
            except Exception as e:
                logger.debug(f"Path traversal test error: {e}")
        
        return findings
    
    async def _send_payload(self, url: str, param: str, payload: str, method: str) -> Optional[Dict]:
        try:
            if method == "GET":
                sep = '&' if '?' in url else '?'
                test_url = f"{url}{sep}{param}={payload}"
                return await self.http_client.get(test_url)
            else:
                return await self.http_client.post(url, data={param: payload})
        except:
            return None
    
    def _has_file_disclosure(self, response: Dict) -> bool:
        """Check if response contains file content"""
        content = response.get('content', '').lower()
        indicators = [
            'root:x:',  # /etc/passwd
            'administrator',  # Windows
            'daemon:',  # Unix/Linux
        ]
        return any(ind in content for ind in indicators)

class XXEDetector:
    """Detect XXE vulnerabilities"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
    
    async def test_xml_endpoint(self, url: str, method: str = "POST") -> List[Dict]:
        """Test XML endpoints for XXE"""
        findings = []
        payloads = PayloadGenerator.get_xxe_payloads()
        
        for payload in payloads[:2]:
            try:
                response = await self.http_client.post(url, data=payload)
                if response and ('DOCTYPE' not in response.get('content', '') or response.get('status') == 200):
                    findings.append({
                        'type': 'XML External Entity (XXE)',
                        'severity': 'HIGH',
                        'url': url,
                        'payload': payload[:50],
                        'evidence': 'XXE payload accepted',
                        'cvss_score': 8.1,
                    })
                    break
            except Exception as e:
                logger.debug(f"XXE test error: {e}")
        
        return findings

class SSRFDetector:
    """Detect SSRF vulnerabilities"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
    
    async def test_url_parameter(
        self,
        url: str,
        param: str,
        method: str = "GET"
    ) -> List[Dict]:
        """Test for SSRF"""
        findings = []
        payloads = PayloadGenerator.get_ssrf_payloads()
        
        for payload in payloads[:3]:
            try:
                response = await self._send_payload(url, param, payload, method)
                if response and self._indicates_ssrf(response):
                    findings.append({
                        'type': 'Server-Side Request Forgery (SSRF)',
                        'severity': 'HIGH',
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'evidence': 'Server appears to have processed URL',
                        'cvss_score': 7.8,
                    })
                    break
            except Exception as e:
                logger.debug(f"SSRF test error: {e}")
        
        return findings
    
    async def _send_payload(self, url: str, param: str, payload: str, method: str) -> Optional[Dict]:
        try:
            if method == "GET":
                sep = '&' if '?' in url else '?'
                test_url = f"{url}{sep}{param}={payload}"
                return await self.http_client.get(test_url)
            else:
                return await self.http_client.post(url, data={param: payload})
        except:
            return None
    
    def _indicates_ssrf(self, response: Dict) -> bool:
        """Check if response indicates SSRF"""
        content = response.get('content', '').lower()
        indicators = [
            'admin',  # /admin access
            'private',  # Private network
            'internal',  # Internal server
        ]
        return any(ind in content for ind in indicators)
