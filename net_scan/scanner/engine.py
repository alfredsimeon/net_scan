"""
NET_SCAN - Main Scanning Engine
Orchestrates crawling, testing, and reporting
"""

import asyncio
import logging
from typing import List, Dict, Optional
from pathlib import Path

from net_scan.scanner.crawler import WebCrawler
from net_scan.scanner.detectors.sql_injection import SQLInjectionDetector
from net_scan.scanner.detectors.xss import XSSDetector
from net_scan.scanner.detectors.csrf import CSRFDetector
from net_scan.scanner.detectors.cmd_injection import CommandInjectionDetector
from net_scan.scanner.detectors.advanced import PathTraversalDetector, XXEDetector, SSRFDetector
from net_scan.utils.http_client import HTTPClient
from net_scan.utils.terminal_ui import TerminalUI
from net_scan.report.generator import ReportGenerator

logger = logging.getLogger(__name__)

class ScannerEngine:
    """Main scanning engine"""
    
    def __init__(
        self,
        target_url: str,
        max_depth: int = 3,
        max_pages: int = 100,
        max_threads: int = 5,
        profile: str = "balanced",
        proxy: Optional[str] = None,
    ):
        self.target_url = target_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.max_threads = max_threads
        self.profile = profile
        self.proxy = proxy
        self.findings: List[Dict] = []
        self.crawled_pages = []
        
        # Configure profile
        self.profile_config = self._get_profile_config(profile)
    
    def _get_profile_config(self, profile: str) -> Dict:
        """Get configuration for profile"""
        profiles = {
            'quick': {
                'max_depth': 2,
                'max_pages': 30,
                'tests': ['sqli', 'xss'],
                'timeout': 15,
            },
            'balanced': {
                'max_depth': 3,
                'max_pages': 100,
                'tests': ['sqli', 'xss', 'csrf', 'cmd', 'path_traversal'],
                'timeout': 30,
            },
            'aggressive': {
                'max_depth': 5,
                'max_pages': 500,
                'tests': ['sqli', 'xss', 'csrf', 'cmd', 'path_traversal', 'xxe', 'ssrf'],
                'timeout': 60,
            },
        }
        
        return profiles.get(profile, profiles['balanced'])
    
    async def run(self) -> List[Dict]:
        """Execute full scan"""
        TerminalUI.print_section("NET_SCAN SECURITY ASSESSMENT")
        TerminalUI.print_status(f"Target: {self.target_url}", "INFO")
        TerminalUI.print_status(f"Profile: {self.profile.upper()}", "INFO")
        
        # Step 1: Crawl website
        TerminalUI.print_section("PHASE 1: SITE CRAWLING")
        crawler = WebCrawler(
            self.target_url,
            max_depth=self.profile_config['max_depth'],
            max_pages=self.profile_config['max_pages'],
        )
        
        self.crawled_pages = await crawler.crawl()
        TerminalUI.print_status(f"Crawled {len(self.crawled_pages)} pages", "SUCCESS")
        
        # Step 2: Run vulnerability tests
        TerminalUI.print_section("PHASE 2: VULNERABILITY TESTING")
        
        async with HTTPClient(timeout=self.profile_config['timeout'], proxy=self.proxy) as http_client:
            endpoints = crawler.get_testable_endpoints()
            total_endpoints = len(endpoints)
            
            # Handle case where no testable endpoints are discovered
            if total_endpoints == 0:
                TerminalUI.print_status("No testable endpoints found on target", "WARNING")
                TerminalUI.print_status("Possible reasons:", "INFO")
                print("  • Target is a static website with no forms or parameters")
                print("  • All parameters are protected or read-only")
                print("  • JavaScript rendering didn't discover dynamic endpoints")
                TerminalUI.print_progress_bar(0, 1, "Testing endpoints...")
                TerminalUI.print_status(f"Found 0 vulnerabilities", "SUCCESS")
                return self.findings
            
            for i, endpoint in enumerate(endpoints):
                TerminalUI.print_progress_bar(i, total_endpoints, "Testing endpoints...")
                
                url = endpoint['url']
                method = endpoint['method']
                parameters = endpoint['parameters']
                
                for param in parameters:
                    # SQL Injection
                    if 'sqli' in self.profile_config['tests']:
                        sqli_detector = SQLInjectionDetector(http_client)
                        sqli_findings = await sqli_detector.test_url_parameter(url, param, method)
                        self.findings.extend(sqli_findings)
                    
                    # XSS
                    if 'xss' in self.profile_config['tests']:
                        xss_detector = XSSDetector(http_client)
                        xss_findings = await xss_detector.test_url_parameter(url, param, method)
                        self.findings.extend(xss_findings)
                    
                    # Command Injection
                    if 'cmd' in self.profile_config['tests']:
                        cmd_detector = CommandInjectionDetector(http_client)
                        cmd_findings = await cmd_detector.test_url_parameter(url, param, method)
                        self.findings.extend(cmd_findings)
                    
                    # Path Traversal
                    if 'path_traversal' in self.profile_config['tests']:
                        path_detector = PathTraversalDetector(http_client)
                        path_findings = await path_detector.test_url_parameter(url, param, method)
                        self.findings.extend(path_findings)
                    
                    # SSRF
                    if 'ssrf' in self.profile_config['tests']:
                        ssrf_detector = SSRFDetector(http_client)
                        ssrf_findings = await ssrf_detector.test_url_parameter(url, param, method)
                        self.findings.extend(ssrf_findings)
                
                # CSRF testing on pages
                if 'csrf' in self.profile_config['tests']:
                    for page in self.crawled_pages:
                        if page.url == url:
                            csrf_detector = CSRFDetector(http_client)
                            csrf_findings = await csrf_detector.test_page(url, page.html)
                            self.findings.extend(csrf_findings)
            
            TerminalUI.print_progress_bar(total_endpoints, total_endpoints, "Testing endpoints...")
        
        TerminalUI.print_status(f"Found {len(self.findings)} vulnerabilities", "WARNING" if self.findings else "SUCCESS")
        
        return self.findings
    
    def generate_reports(self, output_dir: str = "reports") -> Dict[str, str]:
        """Generate reports in multiple formats"""
        TerminalUI.print_section("PHASE 3: REPORT GENERATION")
        
        Path(output_dir).mkdir(exist_ok=True)
        
        # Remove domain for filename
        from urllib.parse import urlparse
        domain = urlparse(self.target_url).netloc.replace('.', '_')
        timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
        
        generator = ReportGenerator(self.findings, self.target_url)
        
        reports = {}
        
        # HTML Report
        html_file = f"{output_dir}/NET_SCAN_{domain}_{timestamp}.html"
        generator.generate_html(html_file)
        reports['html'] = html_file
        TerminalUI.print_status(f"HTML report saved to {html_file}", "SUCCESS")
        
        # JSON Report
        json_file = f"{output_dir}/NET_SCAN_{domain}_{timestamp}.json"
        generator.generate_json(json_file)
        reports['json'] = json_file
        TerminalUI.print_status(f"JSON report saved to {json_file}", "SUCCESS")
        
        # Markdown Report
        md_file = f"{output_dir}/NET_SCAN_{domain}_{timestamp}.md"
        generator.generate_markdown(md_file)
        reports['markdown'] = md_file
        TerminalUI.print_status(f"Markdown report saved to {md_file}", "SUCCESS")
        
        return reports
