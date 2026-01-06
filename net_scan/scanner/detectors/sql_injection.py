"""
NET_SCAN - SQL Injection Detector
Advanced SQL injection testing with multiple techniques
"""

import asyncio
import time
import re
from typing import List, Dict, Optional
import logging
from net_scan.utils.payloads import PayloadGenerator
from net_scan.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)

class SQLInjectionDetector:
    """Detect SQL injection vulnerabilities"""
    
    # Error signatures indicating SQLi
    ERROR_SIGNATURES = {
        'mysql': [
            r"You have an error in your SQL syntax",
            r"mysql_fetch",
            r"Warning.*mysql",
            r"valid MySQL result",
        ],
        'postgres': [
            r"PostgreSQL.*ERROR",
            r"Syntax error.*SQL",
            r"pg_query",
            r"pg_fetch",
        ],
        'mssql': [
            r"Unclosed quotation mark",
            r"Syntax error in SQL",
            r"Microsoft OLE DB",
            r"ODBC.*Driver",
        ],
        'oracle': [
            r"ORA-[0-9]+",
            r"Oracle error",
            r"SQLError",
        ],
        'generic': [
            r"SQL syntax error",
            r"unexpected token",
            r"Unknown column",
            r"syntax error",
        ]
    }
    
    def __init__(self, http_client: HTTPClient, timeout: float = 30):
        self.http_client = http_client
        self.timeout = timeout
        self.findings: List[Dict] = []
    
    async def test_url_parameter(
        self,
        url: str,
        param: str,
        method: str = "GET"
    ) -> List[Dict]:
        """Test URL parameter for SQL injection"""
        findings = []
        
        logger.debug(f"Testing {method} {url}?{param}=<payload> for SQLi")
        
        # Time-based detection
        time_based = await self._test_time_based(url, param, method)
        if time_based:
            findings.extend(time_based)
        
        # Error-based detection
        error_based = await self._test_error_based(url, param, method)
        if error_based:
            findings.extend(error_based)
        
        # Boolean-based detection
        bool_based = await self._test_boolean_based(url, param, method)
        if bool_based:
            findings.extend(bool_based)
        
        return findings
    
    async def _test_time_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Time-based blind SQL injection"""
        findings = []
        payloads = PayloadGenerator.get_sql_payloads("time_based")
        
        for payload in payloads[:3]:  # Test first 3 time-based payloads
            try:
                # Measure baseline response time
                baseline_time = await self._measure_response_time(url, param, "test", method)
                
                # Send payload and measure time
                payload_time = await self._measure_response_time(url, param, payload, method)
                
                # If response takes significantly longer, likely vulnerable
                if payload_time > baseline_time + 4:  # 4+ second difference
                    findings.append({
                        'type': 'SQL Injection (Time-based)',
                        'severity': 'HIGH',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': payload,
                        'evidence': f"Response time increased from {baseline_time:.2f}s to {payload_time:.2f}s",
                        'cvss_score': 8.6,
                    })
                    break
            
            except Exception as e:
                logger.debug(f"Time-based test error: {e}")
        
        return findings
    
    async def _test_error_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Error-based SQL injection"""
        findings = []
        payloads = PayloadGenerator.get_sql_payloads("error_based")
        
        for payload in payloads[:3]:
            try:
                response = await self._send_payload(url, param, payload, method)
                
                if response and self._has_sql_error(response):
                    findings.append({
                        'type': 'SQL Injection (Error-based)',
                        'severity': 'CRITICAL',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': payload,
                        'evidence': 'SQL error message in response',
                        'cvss_score': 9.1,
                    })
                    break
            
            except Exception as e:
                logger.debug(f"Error-based test error: {e}")
        
        return findings
    
    async def _test_boolean_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Boolean-based blind SQL injection"""
        findings = []
        true_payload = "1' AND '1'='1"
        false_payload = "1' AND '1'='2"
        
        try:
            # Get baseline response with normal param
            baseline = await self._send_payload(url, param, "test", method)
            
            # Send true condition
            true_resp = await self._send_payload(url, param, true_payload, method)
            
            # Send false condition
            false_resp = await self._send_payload(url, param, false_payload, method)
            
            if true_resp and false_resp:
                # Check if responses differ significantly
                true_len = len(true_resp.get('content', ''))
                false_len = len(false_resp.get('content', ''))
                
                # If true condition returns more content than false, likely vulnerable
                if true_len > false_len * 1.1:  # 10% difference threshold
                    findings.append({
                        'type': 'SQL Injection (Boolean-based Blind)',
                        'severity': 'HIGH',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': true_payload,
                        'evidence': f"Response length differs: true={true_len}, false={false_len}",
                        'cvss_score': 8.2,
                    })
        
        except Exception as e:
            logger.debug(f"Boolean-based test error: {e}")
        
        return findings
    
    async def _measure_response_time(
        self,
        url: str,
        param: str,
        value: str,
        method: str
    ) -> float:
        """Measure response time for payload"""
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
        """Send payload to parameter"""
        try:
            if method == "GET":
                # Append to URL
                sep = '&' if '?' in url else '?'
                test_url = f"{url}{sep}{param}={payload}"
                return await self.http_client.get(test_url)
            else:
                # POST data
                data = {param: payload}
                return await self.http_client.post(url, data=data)
        except Exception as e:
            logger.debug(f"Payload send error: {e}")
            return None
    
    def _has_sql_error(self, response: Dict) -> bool:
        """Check if response contains SQL error"""
        content = response.get('content', '').lower()
        
        for db_type, signatures in self.ERROR_SIGNATURES.items():
            for sig in signatures:
                if re.search(sig, content, re.IGNORECASE):
                    return True
        
        return False
