# NET_SCAN - Production Deployment Guide

## Overview

NET_SCAN is a production-grade web vulnerability scanner designed for authorized security professionals to identify vulnerabilities before attackers do. It combines intelligent crawling, comprehensive testing, and professional reporting.

## Project Structure

```
net-scan/
├── net_scan/
│   ├── __init__.py                 # Package initialization
│   ├── cli.py                      # Click CLI interface
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── crawler.py              # Web crawler with JS rendering
│   │   ├── engine.py               # Main scanning orchestrator
│   │   └── detectors/              # Vulnerability detectors
│   │       ├── __init__.py
│   │       ├── sql_injection.py    # SQL injection testing
│   │       ├── xss.py              # XSS detection
│   │       ├── csrf.py             # CSRF detection
│   │       ├── cmd_injection.py    # Command injection
│   │       └── advanced.py         # XXE, SSRF, Path traversal
│   ├── report/
│   │   ├── __init__.py
│   │   ├── generator.py            # Multi-format report generation
│   │   └── templates/              # HTML/email templates
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py               # Security logging
│   │   ├── terminal_ui.py          # Retro terminal UI
│   │   ├── http_client.py          # Async HTTP client
│   │   └── payloads.py             # Payload generation
│   ├── config/                     # Scan profiles & payloads
│   └── db/                         # Findings database
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore rules
```

## Vulnerability Detection Capabilities

### 1. SQL Injection (SQLi)
- **Time-based blind** - Measures response time differences
- **Error-based** - Detects SQL error messages
- **Union-based** - Tests UNION query injection
- **Boolean-based blind** - Analyzes true/false responses
- **CVSS Scores:** 8.2 - 9.1

### 2. Cross-Site Scripting (XSS)
- **Reflected XSS** - Tests parameter reflection without encoding
- **DOM XSS** - Tests JavaScript context injection
- **Payload variations:** Script tags, event handlers, attributes
- **CVSS Score:** 7.5

### 3. Cross-Site Request Forgery (CSRF)
- **Token detection** - Checks for CSRF protection
- **SameSite validation** - Verifies cookie attributes
- **Form analysis** - Identifies unprotected state-changing requests
- **CVSS Score:** 6.5

### 4. OS Command Injection
- **Time-based detection** - Measures delay from sleep commands
- **Multiple separators** - Tests `;`, `|`, `||`, `&&`, backticks, `$()`
- **Cross-platform payloads** - Linux and Windows compatible
- **CVSS Score:** 9.8

### 5. Path Traversal
- **Directory traversal** - Tests `../`, `..\\`, encoded variants
- **File disclosure** - Checks for `/etc/passwd`, system file access
- **Multiple encoding** - URL encoding, double encoding, null bytes
- **CVSS Score:** 7.5

### 6. XML External Entity (XXE)
- **File disclosure** - Attempts to read local files
- **Blind XXE** - Out-of-band data exfiltration
- **XXE bombs** - Billion laughs attack detection
- **CVSS Score:** 8.1

### 7. Server-Side Request Forgery (SSRF)
- **Internal network access** - Probes localhost, private IPs
- **Metadata endpoints** - Tests cloud metadata services
- **Protocol testing** - HTTP, file, gopher, dict schemes
- **CVSS Score:** 7.8

## Advanced Features

### Intelligent Crawling
- **JavaScript rendering** - Uses Playwright for dynamic content
- **Session management** - Maintains cookies across requests
- **Form detection** - Identifies and analyzes HTML forms
- **Parameter extraction** - Collects all testable input points
- **Rate limiting** - Respects server load
- **URL deduplication** - Prevents redundant testing

### Smart Testing
- **Context-aware payloads** - Adjusts tests based on parameter type
- **Payload obfuscation** - WAF bypass techniques
- **Response analysis** - Pattern matching and heuristics
- **False positive reduction** - Multi-stage validation
- **Concurrency** - Multi-threaded efficient testing

### Professional Reporting
- **HTML reports** - Interactive with charts and severity breakdown
- **JSON export** - API and automation integration
- **Markdown format** - Version control and documentation
- **CVSS scoring** - Industry-standard vulnerability assessment
- **Remediation steps** - Actionable security recommendations
- **Security references** - OWASP and CWE links

### Terminal UI
- **ASCII art banner** - Retro aesthetic
- **Progress tracking** - Real-time scanning updates
- **Color coding** - Severity-based visual indicators
- **Animations** - Professional, polished CLI experience

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- 500 MB free disk space (for Playwright browsers)
- Windows, Linux, or macOS

### Installation Steps - Using Virtual Environment (Recommended)

Virtual environments isolate NET_SCAN dependencies and prevent pip issues.

#### Windows (PowerShell)

```powershell
# 1. Navigate to project
cd net-scan

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
.\\venv\\Scripts\\Activate.ps1

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install Playwright browsers
python -m playwright install

# 7. Install NET_SCAN
pip install -e .

# 8. Verify installation
net-scan --version
```

#### Linux/macOS (Bash)

```bash
# 1. Navigate to project
cd net-scan

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Upgrade pip
python3 -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install Playwright browsers
python -m playwright install

# 7. Install NET_SCAN
pip install -e .

# 8. Verify installation
net-scan --version
```

### Alternative: System-Wide Installation (Not Recommended)

If you cannot use virtual environments:

```bash
# Windows
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
pip install -e .

# Linux/macOS
python3 -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
pip install -e .
```

⚠️ **Warning:** System-wide installation can cause conflicts. See [VENV_SETUP.md](VENV_SETUP.md) for troubleshooting.

## Usage Examples

### Basic Scan (Remember to activate venv first)

```powershell
# Windows - activate venv
.\\venv\\Scripts\\Activate.ps1
net-scan scan https://target.com
```

```bash
# Linux/macOS - activate venv
source venv/bin/activate
net-scan scan https://target.com
```

### With Proxy (Burp Suite)
```powershell
# Windows
.\\venv\\Scripts\\Activate.ps1
net-scan scan https://target.com --proxy http://localhost:8080
```

```bash
# Linux/macOS
source venv/bin/activate
net-scan scan https://target.com --proxy http://localhost:8080
```

### Specific Tests Only
```powershell
# Windows
.\\venv\\Scripts\\Activate.ps1
net-scan scan https://target.com --tests sqli,xss,csrf
```

```bash
# Linux/macOS
source venv/bin/activate
net-scan scan https://target.com --tests sqli,xss,csrf
```

### Custom Configuration
```powershell
# Windows
.\\venv\\Scripts\\Activate.ps1
net-scan scan https://target.com `
  --profile aggressive `
  --depth 5 `
  --max-pages 200 `
  --threads 10
```

```bash
# Linux/macOS
source venv/bin/activate
net-scan scan https://target.com \
  --profile aggressive \
  --depth 5 \
  --max-pages 200 \
  --threads 10
```

### Interactive Mode
```powershell
# Windows
.\\venv\\Scripts\\Activate.ps1
net-scan interactive
```

```bash
# Linux/macOS
source venv/bin/activate
net-scan interactive
```

## Scan Profiles

### Quick Profile (5 minutes)
- Crawl depth: 2 levels
- Pages scanned: 30 max
- Tests: SQLi, XSS only
- Best for: Initial reconnaissance

### Balanced Profile (15 minutes - Default)
- Crawl depth: 3 levels
- Pages scanned: 100 max
- Tests: SQLi, XSS, CSRF, Command Injection, Path Traversal
- Best for: Standard security assessments

### Aggressive Profile (45+ minutes)
- Crawl depth: 5 levels
- Pages scanned: 500 max
- Tests: All vulnerability types
- Best for: Comprehensive deep security audits

## Report Output

### Report Files

All reports are generated with timestamp and domain name:
- `NET_SCAN_example_com_20260106_120000.html` - Interactive HTML
- `NET_SCAN_example_com_20260106_120000.json` - Machine-readable JSON
- `NET_SCAN_example_com_20260106_120000.md` - Markdown format

### Report Contents

Each report includes:

1. **Executive Summary**
   - Target URL and scan date
   - Total findings count
   - Severity breakdown (Critical, High, Medium, Low)

2. **Detailed Findings**
   - Vulnerability type
   - Affected URL and parameter
   - HTTP method
   - CVSS score
   - Evidence/Proof of concept
   - Payload used

3. **Remediation Guidance**
   - Vulnerability description
   - Step-by-step fix instructions
   - Security best practices
   - OWASP and CWE references

4. **Visual Elements** (HTML only)
   - Severity distribution charts
   - Color-coded findings
   - Interactive navigation

## Security Considerations

### For Users
✓ Only scan systems you own or have written permission to test
✓ Obtain written authorization before assessments
✓ Use staging environments for testing
✓ Keep scan reports confidential
✓ Review findings with your security team

### For the Tool
✓ Sensitive data is redacted in logs
✓ No data is sent to external servers
✓ SSL verification can be configured
✓ Proxy support for traffic inspection
✓ Secure error handling

### Legal Disclaimer
NET_SCAN is designed for authorized security testing only. Unauthorized testing is illegal and unethical. Always:
- Obtain written permission
- Comply with applicable laws
- Respect privacy and data protection
- Use responsibly and ethically

## Performance Optimization

### For Large Sites
```bash
# Reduce scope to improve speed
net-scan scan https://large-site.com \
  --profile quick \
  --max-pages 50 \
  --depth 2
```

### For Thorough Testing
```bash
# Allow more time for comprehensive testing
net-scan scan https://target.com \
  --profile aggressive \
  --threads 10 \
  --timeout 60
```

### Resource Usage
- **Memory:** 200-500 MB typical
- **CPU:** Multi-threaded, scalable
- **Network:** Variable based on target size
- **Storage:** ~1-5 MB per report

## Troubleshooting

### Playwright Installation Fails
```bash
# Ensure system dependencies are installed
# On Ubuntu/Debian:
sudo apt-get install -y gconf-service libasound2 libatk1.0-0 libgbm1

# On Windows: Download latest Python and reinstall
pip uninstall playwright -y
pip install playwright
playwright install
```

### Timeout Issues
- Increase `--timeout` value
- Reduce `--max-pages` or `--depth`
- Check network connectivity

### Proxy Connection Failed
- Verify proxy is running (Burp, ZAP)
- Check correct port number
- Test: `curl --proxy http://localhost:8080 https://example.com`

## Integration & Automation

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Run NET_SCAN
  run: |
    net-scan scan https://app.example.com \
      --profile balanced \
      --report-dir ./security-reports
```

### Webhook Notifications
```python
# Example: Trigger alerts on critical findings
import json
findings = json.load(open('NET_SCAN_*.json'))
if any(f['severity'] == 'CRITICAL' for f in findings['findings']):
    send_alert("Critical vulnerability found!")
```

### Database Storage
```python
# Store findings in database for tracking
import sqlite3
conn = sqlite3.connect('vulnerabilities.db')
# Insert findings with timestamps for trend analysis
```

## Support & Documentation

- **README.md** - Full feature documentation
- **QUICKSTART.md** - Quick start guide
- **Inline code comments** - Implementation details
- **Error logs** - Debug information in logs/ directory

## Version History

- **v1.0.0** (2026-01-06) - Initial release
  - Core vulnerability detection
  - Multi-format reporting
  - Professional CLI interface
  - Production-ready code quality

## License

MIT License - See LICENSE file for details

---

**NET_SCAN v1.0.0**
Production-Grade Web Vulnerability Scanner
© 2026 Fred (alfredsimeon)

GitHub Repository: https://github.com/alfredsimeon/net_scan
Author Profile: https://github.com/alfredsimeon

**Remember:** Use responsibly. Unauthorized testing is illegal.
