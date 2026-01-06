"""
NET_SCAN - SQL Injection Detector
Advanced SQL injection testing with multiple techniques and WAF bypass
"""

import asyncio
import time
import re
from typing import List, Dict, Optional
import logging
from urllib.parse import quote, urljoin
from net_scan.utils.payloads import PayloadGenerator
from net_scan.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)

class SQLInjectionDetector:
    """Detect SQL injection vulnerabilities with advanced techniques"""
    
    # Error signatures indicating SQLi
    ERROR_SIGNATURES = {
        'mysql': [
            r"You have an error in your SQL syntax",
            r"mysql_fetch",
            r"Warning.*mysql",
            r"valid MySQL result",
            r"MySQL Query",
            r"mysql_num_rows",
        ],
        'postgres': [
            r"PostgreSQL.*ERROR",
            r"Syntax error.*SQL",
            r"pg_query",
            r"pg_fetch",
            r"PG::SyntaxError",
        ],
        'mssql': [
            r"Unclosed quotation mark",
            r"Syntax error in SQL",
            r"Microsoft OLE DB",
            r"ODBC.*Driver",
            r"Level 15, State 1",
        ],
        'oracle': [
            r"ORA-[0-9]+",
            r"Oracle error",
            r"SQLError",
            r"Exception in thread",
        ],
        'generic': [
            r"SQL syntax error",
            r"unexpected token",
            r"Unknown column",
            r"syntax error",
            r"database error",
            r"sql error",
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
        """Test URL parameter for SQL injection with multiple techniques"""
        findings = []
        
        logger.debug(f"Testing {method} {url}?{param}=<payload> for SQLi")
        
        # Test with original and encoded variations
        for variation in [url, self._obfuscate_url(url)]:
            # Time-based blind SQLi (works against most databases)
            time_based = await self._test_time_based(variation, param, method)
            if time_based:
                return time_based  # Return immediately if found
            
            # Error-based SQLi (fastest if it works)
            error_based = await self._test_error_based(variation, param, method)
            if error_based:
                return error_based
            
            # Boolean-based blind SQLi
            bool_based = await self._test_boolean_based(variation, param, method)
            if bool_based:
                return bool_based
            
            # Union-based SQLi (most reliable)
            union_based = await self._test_union_based(variation, param, method)
            if union_based:
                return union_based
        
        return findings
    
    def _obfuscate_url(self, url: str) -> str:
        """Create obfuscated version of URL to bypass simple WAF rules"""
        # Add space encodings, case variations, etc
        return url  # Base implementation - can extend
    
    async def _test_union_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Union-based SQL injection (most reliable)"""
        findings = []
        payloads = PayloadGenerator.get_sql_payloads("union_based")
        
        for payload in payloads[:2]:  # Test first 2 union payloads
            try:
                response = await self._send_payload(url, param, payload, method)
                
                if response and self._has_sql_error(response):
                    findings.append({
                        'type': 'SQL Injection (Union-based)',
                        'severity': 'CRITICAL',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': payload,
                        'evidence': 'SQL error message indicating union injection',
                        'cvss_score': 9.1,
                        'remediation': 'Use parameterized queries/prepared statements',
                        'cwe': 'CWE-89'
                    })
                    return findings
            
            except Exception as e:
                logger.debug(f"Union-based test error: {e}")
        
        return findings
    
    async def _test_time_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Time-based blind SQL injection with multiple payloads"""
        findings = []
        payloads = PayloadGenerator.get_sql_payloads("time_based")
        
        # Test each payload type
        for payload in payloads[:2]:  # Test first 2 time-based payloads
            try:
                # Measure baseline response time (with non-delayed payload)
                baseline_times = []
                for _ in range(2):
                    baseline_time = await self._measure_response_time(url, param, "1", method)
                    baseline_times.append(baseline_time)
                    await asyncio.sleep(0.1)
                
                baseline_avg = sum(baseline_times) / len(baseline_times)
                
                # Send time-delay payload
                payload_time = await self._measure_response_time(url, param, payload, method)
                
                # If response takes significantly longer (>4 seconds), likely vulnerable
                time_diff = payload_time - baseline_avg
                
                if time_diff > 3 and payload_time > 4:  # At least 3 second difference AND >4s total
                    findings.append({
                        'type': 'SQL Injection (Time-based Blind)',
                        'severity': 'HIGH',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': payload,
                        'evidence': f"Response time: baseline={baseline_avg:.2f}s, with payload={payload_time:.2f}s (diff={time_diff:.2f}s)",
                        'cvss_score': 8.6,
                        'remediation': 'Use parameterized queries/prepared statements',
                        'cwe': 'CWE-89'
                    })
                    return findings
            
            except Exception as e:
                logger.debug(f"Time-based test error for {payload}: {e}")
        
        return findings
    
    async def _test_error_based(
        self,
        url: str,
        param: str,
        method: str
    ) -> List[Dict]:
        """Error-based SQL injection with multiple techniques"""
        findings = []
        payloads = PayloadGenerator.get_sql_payloads("error_based")
        
        baseline_response = await self._send_payload(url, param, "test", method)
        baseline_content = baseline_response.get('content', '') if baseline_response else ""
        baseline_has_error = self._has_sql_error(baseline_response) if baseline_response else False
        
        for payload in payloads[:3]:
            try:
                response = await self._send_payload(url, param, payload, method)
                
                if not response:
                    continue
                
                current_content = response.get('content', '')
                current_has_error = self._has_sql_error(response)
                
                # Only flag as SQLi if:
                # 1. Error appears AFTER payload (wasn't in baseline)
                # 2. AND error is clearly database-related
                # 3. AND response changed significantly from baseline
                if (current_has_error and not baseline_has_error and 
                    len(current_content) != len(baseline_content)):
                    
                    findings.append({
                        'type': 'SQL Injection (Error-based)',
                        'severity': 'CRITICAL',
                        'url': url,
                        'parameter': param,
                        'method': method,
                        'payload': payload,
                        'evidence': 'SQL error message in response revealing database structure',
                        'cvss_score': 9.1,
                        'remediation': 'Use parameterized queries/prepared statements and disable error display',
                        'cwe': 'CWE-89'
                    })
                    return findings
            
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
                
                # Guard against zero-length responses - need minimum response data to compare
                if false_len == 0:
                    logger.debug(f"Empty response for boolean-based SQLi test: {url}")
                else:
                    # If true condition returns more content than false, likely vulnerable
                    if true_len > 0 and true_len > false_len * 1.1:  # 10% difference threshold
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
