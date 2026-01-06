"""
NET_SCAN - Command Line Interface
Main CLI entry point with Click
"""

import asyncio
import click
from pathlib import Path
import logging
from typing import Optional

from net_scan.scanner.engine import ScannerEngine
from net_scan.utils.terminal_ui import TerminalUI
from net_scan.utils.logger import logger as security_logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """NET_SCAN - Production-Grade Web Vulnerability Scanner"""
    pass

@cli.command()
@click.argument('url')
@click.option('--profile', type=click.Choice(['quick', 'balanced', 'aggressive']), default='balanced',
              help='Scan profile: quick (5 min), balanced (15 min), aggressive (45+ min)')
@click.option('--depth', type=int, default=3, help='Maximum crawl depth')
@click.option('--max-pages', type=int, default=100, help='Maximum pages to crawl')
@click.option('--threads', type=int, default=5, help='Number of concurrent threads')
@click.option('--timeout', type=int, default=30, help='Request timeout in seconds')
@click.option('--proxy', type=str, help='HTTP proxy URL (e.g., http://localhost:8080)')
@click.option('--tests', type=str, help='Specific tests to run (comma-separated: sqli,xss,csrf,cmd,path,xxe,ssrf)')
@click.option('--report-dir', type=str, default='reports', help='Directory for reports')
@click.option('--no-report', is_flag=True, help='Skip report generation')
def scan(
    url: str,
    profile: str,
    depth: int,
    max_pages: int,
    threads: int,
    timeout: int,
    proxy: Optional[str],
    tests: Optional[str],
    report_dir: str,
    no_report: bool,
):
    """
    Scan a web application for vulnerabilities
    
    Example:
        net-scan scan https://example.com
        net-scan scan https://example.com --profile aggressive
        net-scan scan https://example.com --proxy http://localhost:8080
    """
    try:
        # Print banner
        TerminalUI.print_banner()
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        logger.info(f"Starting scan for {url}")
        
        # Create scanner engine
        scanner = ScannerEngine(
            target_url=url,
            max_depth=depth,
            max_pages=max_pages,
            max_threads=threads,
            profile=profile,
            proxy=proxy,
        )
        
        # Run scan
        findings = asyncio.run(scanner.run())
        
        # Print summary
        TerminalUI.print_section("SCAN SUMMARY")
        TerminalUI.print_status(f"Total vulnerabilities found: {len(findings)}", 
                               "WARNING" if findings else "SUCCESS")
        
        # Count by severity
        severity_counts = {
            'CRITICAL': len([f for f in findings if f.get('severity') == 'CRITICAL']),
            'HIGH': len([f for f in findings if f.get('severity') == 'HIGH']),
            'MEDIUM': len([f for f in findings if f.get('severity') == 'MEDIUM']),
            'LOW': len([f for f in findings if f.get('severity') == 'LOW']),
        }
        
        click.echo(f"\n{click.style('Severity Breakdown:', fg='cyan')}")
        for severity, count in severity_counts.items():
            if severity == 'CRITICAL':
                color = 'red'
            elif severity == 'HIGH':
                color = 'red'
            elif severity == 'MEDIUM':
                color = 'yellow'
            else:
                color = 'green'
            click.echo(f"  {click.style(severity, fg=color)}: {count}")
        
        # Print findings summary
        if findings:
            click.echo(f"\n{click.style('Top Vulnerabilities:', fg='cyan')}")
            for i, finding in enumerate(findings[:5], 1):
                severity_color = {
                    'CRITICAL': 'red',
                    'HIGH': 'red',
                    'MEDIUM': 'yellow',
                    'LOW': 'green',
                }.get(finding.get('severity'), 'white')
                
                click.echo(f"  {i}. {click.style(finding.get('type', 'Unknown'), fg=severity_color)} "
                          f"({click.style(finding.get('severity', 'UNKNOWN'), fg=severity_color)})")
                click.echo(f"     URL: {finding.get('url', 'N/A')}")
        
        # Generate reports
        if not no_report:
            reports = scanner.generate_reports(report_dir)
            
            click.echo(f"\n{click.style('Reports Generated:', fg='cyan')}")
            for report_type, file_path in reports.items():
                click.echo(f"  ✓ {report_type.upper()}: {file_path}")
        
        TerminalUI.print_section("SCAN COMPLETE")
        click.echo(f"{click.style('[+] Scan completed successfully!', fg='green')}")
        
    except KeyboardInterrupt:
        click.echo(f"\n{click.style('[-] Scan interrupted by user', fg='red')}")
        exit(1)
    except Exception as e:
        click.echo(f"{click.style('[-] Error during scan:', fg='red')} {str(e)}")
        logger.error(f"Scan error: {e}", exc_info=True)
        exit(1)

@cli.command()
@click.option('--url', prompt='Target URL', help='URL to scan')
@click.option('--profile', type=click.Choice(['quick', 'balanced', 'aggressive']), 
              default='balanced', help='Scan profile')
def interactive(url: str, profile: str):
    """Interactive scanning mode"""
    TerminalUI.print_banner()
    click.echo(f"\n{click.style('Interactive Mode', fg='cyan')}")
    click.echo("This mode allows you to configure and run a scan interactively.\n")
    
    # Get options interactively
    depth = click.prompt('Max crawl depth', type=int, default=3)
    max_pages = click.prompt('Max pages to crawl', type=int, default=100)
    threads = click.prompt('Number of threads', type=int, default=5)
    
    click.echo(f"\n{click.style('Starting scan...', fg='green')}\n")
    
    scanner = ScannerEngine(
        target_url=url,
        max_depth=depth,
        max_pages=max_pages,
        max_threads=threads,
        profile=profile,
    )
    
    findings = asyncio.run(scanner.run())
    reports = scanner.generate_reports()
    
    click.echo(f"\n{click.style('✓ Scan complete!', fg='green')}")

@cli.command()
@click.pass_context
def version(ctx):
    """Show version information"""
    click.echo(click.style("NET_SCAN v1.0.0", fg="green", bold=True))
    click.echo("Production-Grade Web Vulnerability Scanner")
    click.echo("Author: Fred (alfredsimeon)")
    ctx.exit(0)

@cli.command()
def config():
    """Show configuration information"""
    click.echo(f"{click.style('NET_SCAN Configuration', fg='cyan')}\n")
    
    click.echo(f"{click.style('Available Scan Profiles:', fg='green')}")
    click.echo("  quick      - Fast scan (5 minutes, basic tests)")
    click.echo("  balanced   - Default (15 minutes, comprehensive)")
    click.echo("  aggressive - Extensive (45+ minutes, advanced tests)\n")
    
    click.echo(f"{click.style('Available Tests:', fg='green')}")
    click.echo("  sqli           - SQL Injection")
    click.echo("  xss            - Cross-Site Scripting")
    click.echo("  csrf           - Cross-Site Request Forgery")
    click.echo("  cmd            - OS Command Injection")
    click.echo("  path_traversal - Path Traversal")
    click.echo("  xxe            - XML External Entity")
    click.echo("  ssrf           - Server-Side Request Forgery\n")
    
    click.echo(f"{click.style('Example Commands:', fg='yellow')}")
    click.echo("  net-scan scan https://example.com")
    click.echo("  net-scan scan https://example.com --profile aggressive")
    click.echo("  net-scan scan https://example.com --proxy http://localhost:8080")
    click.echo("  net-scan scan https://example.com --tests sqli,xss")

def main():
    """Main entry point"""
    try:
        cli()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        exit(1)

if __name__ == '__main__':
    main()
