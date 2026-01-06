# NET_SCAN - Web Vulnerability Scanner

**Production-grade vulnerability scanner for identifying security flaws before attackers do.**

## Overview

NET_SCAN is an advanced, automated web application vulnerability scanner designed for security professionals and penetration testers. It combines intelligent crawling, comprehensive vulnerability testing, and professional reporting to deliver actionable security insights.

## Features

### Advanced Vulnerability Detection
- **SQL Injection** (Time-based, Error-based, Union-based, Blind)
- **Cross-Site Scripting (XSS)** (Reflected, Stored, DOM-based)
- **CSRF** (Cross-Site Request Forgery)
- **Command Injection** (OS command execution)
- **Path Traversal** (Directory traversal, File inclusion)
- **XXE** (XML External Entity attacks)
- **SSRF** (Server-Side Request Forgery)
- **Insecure Deserialization**
- **File Upload Vulnerabilities**
- **Open Redirects**
- **Security Headers Analysis**
- **API Endpoint Enumeration**

### Intelligent Crawling
- JavaScript rendering support (Headless browser)
- Session/Cookie management
- Authentication support (Basic, Form-based)
- Robots.txt & Sitemap.xml parsing
- Crawl depth limiting & URL filtering
- Rate limiting & throttling
- User-Agent rotation

### Professional Reporting
- HTML reports with charts and severity breakdown
- JSON export for automation
- Markdown summaries
- CVSS scoring for each vulnerability
- Remediation recommendations
- Executive summaries

### Terminal UI
- Vintage retro terminal aesthetic
- Real-time progress tracking
- Color-coded severity levels
- ASCII animations
- Vulnerability count updates

## Installation

### Prerequisites
- Python 3.11+
- Pip

### Setup

```bash
# Clone or extract the repository
cd net-scan

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install NET_SCAN
pip install -e .
```

## Quick Start

```bash
# Basic scan
net-scan scan https://target.com

# Aggressive scan with custom threads
net-scan scan https://target.com --profile aggressive --threads 10

# Specific vulnerability tests
net-scan scan https://target.com --tests sqli,xss,csrf

# With proxy (Burp Suite, ZAP)
net-scan scan https://target.com --proxy http://localhost:8080

# Generate report in multiple formats
net-scan scan https://target.com --report html,json,markdown

# Interactive mode
net-scan interactive

# View detailed help
net-scan scan --help
```

## Configuration

### Scan Profiles

- **quick**: Fast scan, basic tests only (~5 minutes)
- **balanced**: Default, comprehensive testing (~15 minutes)
- **aggressive**: Extensive testing, includes advanced techniques (~45 minutes)
- **custom**: User-defined payload and test configuration

### Custom Configuration

Edit `config/scan_profiles.yaml` to customize:
- Payload dictionaries
- Thread counts
- Timeout values
- Test parameters
- Exclusion patterns

## Report Output

Reports are generated in:
- **HTML**: Interactive, browser-viewable with charts
- **JSON**: Machine-readable, automation-friendly
- **Markdown**: Text-based, version-control friendly
- **PDF**: Executive summaries (optional)

## Security Considerations

- NET_SCAN should only be used on systems you own or have explicit permission to test
- Always obtain written authorization before scanning
- Use `--dry-run` mode to preview targets without testing
- Proxy all traffic through your own test infrastructure when possible
- Review findings carefully; some may require manual verification

## Architecture

```
net-scan/
├── scanner/
│   ├── crawler.py          # Site crawling engine
│   ├── engine.py           # Test execution
│   ├── analyzer.py         # Response analysis
│   └── detectors/          # Vulnerability modules
├── report/
│   ├── generator.py        # Report generation
│   ├── severity.py         # CVSS scoring
│   └── templates/          # HTML templates
├── utils/
│   ├── http_client.py      # HTTP handling
│   ├── terminal_ui.py      # Terminal animations
│   ├── payloads.py         # Payload generation
│   └── logger.py           # Logging
├── config/                 # Profiles and payloads
├── db/                     # Database storage
└── cli.py                  # CLI interface
```

## Performance

- Multi-threaded/async scanning
- Intelligent payload ordering
- Response caching
- Connection pooling
- Memory-efficient streaming

## Compliance

- Designed for authorized security testing
- OWASP Top 10 coverage
- CVSS v3.1 severity scoring
- GDPR-compliant data handling

## License

MIT License - See LICENSE file

## Author

**Fred (alfredsimeon)** - Creator and Maintainer
- GitHub: https://github.com/alfredsimeon
- Repository: https://github.com/alfredsimeon/net_scan

## Support

For issues, features, or questions:
- GitHub Repository: https://github.com/alfredsimeon/net_scan
- Create an issue in the repository
- Visit: https://github.com/alfredsimeon

---

**DISCLAIMER**: This tool is provided for authorized security testing only. Unauthorized access to computer systems is illegal. Always obtain written permission before scanning.
