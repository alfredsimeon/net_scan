"""
NET_SCAN - CSRF Detector
Cross-Site Request Forgery vulnerability detection
"""

import re
from typing import List, Dict
import logging
from bs4 import BeautifulSoup
from net_scan.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)

class CSRFDetector:
    """Detect CSRF vulnerabilities"""
    
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.findings: List[Dict] = []
    
    async def test_page(self, url: str, html: str) -> List[Dict]:
        """Test page for CSRF vulnerabilities"""
        findings = []
        
        logger.debug(f"Testing {url} for CSRF vulnerabilities")
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Find all forms
        for form in soup.find_all('form'):
            form_action = form.get('action', '')
            form_method = form.get('method', 'GET').upper()
            
            # Check if form modifies state (POST, PUT, DELETE)
            if form_method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                # Check for CSRF token
                has_csrf_token = self._has_csrf_token(form)
                has_samesite = self._check_samesite_cookie(form)
                
                if not has_csrf_token:
                    findings.append({
                        'type': 'Cross-Site Request Forgery (CSRF)',
                        'severity': 'MEDIUM',
                        'url': url,
                        'form_action': form_action,
                        'form_method': form_method,
                        'evidence': 'Form lacks CSRF token protection',
                        'cvss_score': 6.5,
                    })
        
        return findings
    
    def _has_csrf_token(self, form) -> bool:
        """Check if form has CSRF token"""
        csrf_patterns = [
            'csrf', 'token', 'nonce', '_token', 'authenticity_token',
            'request_token', 'state', 'verification_token'
        ]
        
        # Check for hidden inputs
        for hidden in form.find_all('input', type='hidden'):
            name = hidden.get('name', '').lower()
            for pattern in csrf_patterns:
                if pattern in name:
                    return True
        
        return False
    
    def _check_samesite_cookie(self, form) -> bool:
        """Check if form relies on SameSite cookies"""
        # This would require access to response headers
        # Placeholder for cookie analysis
        return False
