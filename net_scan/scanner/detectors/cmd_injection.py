"""
NET_SCAN - Command Injection Detector
OS command injection vulnerability detection
"""

import time
from typing import List, Dict, Optional
import logging
from net_scan.utils.payloads import PayloadGenerator
from net_scan.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)

class CommandInjectionDetector:
    """Detect command injection vulnerabilities"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.findings: List[Dict] = []
    
    async def test_url_parameter(
        self,
        url: str,
        param: str,
        method: str = "GET"
    ) -> List[Dict]:
        """Test URL parameter for command injection"""
        findings = []
        
        logger.debug(f"Testing {method} {url}?{param}=<payload> for command injection")
        
        # Time-based command injection
        time_based = await self._test_time_based(url, param, method)
        if time_based:
            findings.extend(time_based)
        
        return findings
    
    async def _test_time_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Time-based command injection detection"""
        findings = []
        
        payloads = [
            "; sleep 5",
            "| sleep 5",
            "& timeout 5",
            "&& timeout 5",
        ]
        
        for payload in payloads:
            try:
                baseline_time = await self._measure_response_time(url, param, "test", method)
                payload_time = await self._measure_response_time(url, param, payload, method)
                
                if payload_time > baseline_time + 4:
                    findings.append({
                        'type': 'OS Command Injection',
                        'severity': 'CRITICAL',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': payload,
                        'evidence': f"Response time increased significantly",
                        'cvss_score': 9.8,
                    })
                    break
            except Exception as e:
                logger.debug(f"Command injection test error: {e}")
        
        return findings
    
    async def _measure_response_time(
        self,
        url: str,
        param: str,
        value: str,
        method: str
    ) -> float:
        """Measure response time"""
        try:
            start = time.time()
            await self._send_payload(url, param, value, method)
            return time.time() - start
        except:
            return 0.0
    
    async def _send_payload(
        self,
        url: str,
        param: str,
        payload: str,
        method: str
    ) -> Optional[Dict]:
        """Send command injection payload"""
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
