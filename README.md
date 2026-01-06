# NET_SCAN - Web Vulnerability Scanner

**Production-grade web vulnerability scanner for identifying security flaws before attackers do.**

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup & Activation](#setup--activation)
- [Verification](#verification)
- [Usage Walkthrough](#usage-walkthrough)
- [Scan Profiles](#scan-profiles)
- [Advanced Configuration](#advanced-configuration)
- [Report Output](#report-output)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Security & Legal](#security--legal)
- [About](#about)

---

## Overview

NET_SCAN is an advanced, automated web application vulnerability scanner designed for security professionals and penetration testers. It combines intelligent crawling, comprehensive vulnerability testing, and professional reporting to deliver actionable security insights.

### What This Tool Does

NET_SCAN automatically identifies **7 critical vulnerability types**:

1. **SQL Injection (SQLi)** - Database attack vectors
   - Time-based blind, error-based, union-based, boolean-based blind
   - CVSS: 8.2-9.1

2. **Cross-Site Scripting (XSS)** - JavaScript injection attacks
   - Reflected, stored, and DOM-based XSS detection
   - CVSS: 7.5

3. **Cross-Site Request Forgery (CSRF)** - Request forgery attacks
   - Token detection and SameSite validation
   - CVSS: 6.5

4. **OS Command Injection** - Operating system command execution
   - Time-based detection with multiple separators
   - CVSS: 9.8

5. **Path Traversal** - Unauthorized file system access
   - Directory traversal and file disclosure testing
   - CVSS: 7.5

6. **XML External Entity (XXE)** - XML-based attacks
   - File disclosure and blind XXE testing
   - CVSS: 8.1

7. **Server-Side Request Forgery (SSRF)** - Internal network access
   - Metadata endpoint and protocol testing
   - CVSS: 7.8

---

## Features

### Advanced Vulnerability Detection
- **7 vulnerability types** with multiple detection techniques
- **Context-aware payloads** - Adjusts tests based on parameter type
- **Multi-stage validation** - Reduces false positives
- **WAF bypass techniques** - Payload obfuscation and encoding
- **Response pattern analysis** - Intelligent heuristics

### Intelligent Crawling
- **JavaScript rendering** - Headless browser with Playwright
- **Session management** - Maintains cookies across requests
- **Form detection** - Identifies and analyzes HTML forms
- **Dynamic content** - Handles AJAX and dynamic page loads
- **Authentication support** - Basic and form-based auth
- **Rate limiting** - Respects server load
- **URL deduplication** - Prevents redundant testing
- **Robots.txt & Sitemap parsing** - Intelligent discovery

### Professional Reporting
- **HTML Reports** - Interactive, browser-viewable with charts and severity breakdown
- **JSON Export** - Machine-readable for automation and integration
- **Markdown Summaries** - Version-control friendly text format
- **CVSS Scoring** - Industry-standard vulnerability assessment (CVSS v3.1)
- **Remediation Steps** - Actionable security recommendations
- **Security References** - OWASP and CWE links
- **Executive Summaries** - High-level vulnerability overview

### Terminal UI
- **Vintage retro aesthetic** - ASCII art banner and animations
- **Real-time progress tracking** - Live scanning updates
- **Color-coded severity** - Visual vulnerability indicators
- **Professional output** - Clean, polished CLI experience

### Performance Optimization
- **Multi-threaded/async scanning** - Concurrent vulnerability testing
- **Intelligent payload ordering** - Optimal test sequencing
- **Response caching** - Reduces redundant requests
- **Connection pooling** - Efficient network resource usage
- **Memory-efficient streaming** - Handles large responses

---

## Prerequisites

- **Python 3.11 or higher**
- **pip** (Python package manager)
- **500 MB free disk space** (for Playwright browsers)
- **Windows, Linux, or macOS** operating system

### System Dependencies (Linux/macOS)

**Linux users must install system libraries before installing Python dependencies.**

#### Kali Linux (Latest - Python 3.13) - Playwright JavaScript Rendering

**Step 1: Update and install Python with build tools**
```bash
sudo apt update
sudo apt install -y python3-dev python3-venv build-essential gcc g++ curl wget git
```

**Step 2: Install Chromium browser and Playwright dependencies**
```bash
sudo apt install -y chromium-browser chromium
```

**Step 3: Install system libraries for JavaScript rendering**
```bash
sudo apt install -y libnss3 libnspr4 libx11-6 libxext6 libxrender1 libxrandr2 libgbm1 libdrm2 libdbus-1-3 libexpat1 libssl3 libcups2 libpulse0
```

**Step 4: Install libraries for XML parsing (lxml)**
```bash
sudo apt install -y libxml2 libxml2-dev libxslt1.1 libxslt1-dev zlib1g-dev
```

**Step 5: Install Rust (required for pydantic-core compilation)**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
```

**Step 6: Create virtual environment and install Python packages**
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Step 7: Install Playwright browsers**
```bash
python -m playwright install chromium
```

**Step 8: Install NET_SCAN package**
```bash
pip install -e .
```

**Step 9: Verify installation**
```bash
net-scan --version
net-scan config
```

**All-in-One Installation (if you prefer one command):**
```bash
# Run all apt install commands at once
sudo apt update && \
sudo apt install -y python3-dev python3-venv build-essential gcc g++ curl wget git && \
sudo apt install -y chromium-browser chromium && \
sudo apt install -y libnss3 libnspr4 libx11-6 libxext6 libxrender1 libxrandr2 libgbm1 libdrm2 libdbus-1-3 libexpat1 libssl3 libcups2 libpulse0 && \
sudo apt install -y libxml2 libxml2-dev libxslt1.1 libxslt1-dev zlib1g-dev && \
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
source $HOME/.cargo/env && \
python3 -m venv venv && \
source venv/bin/activate && \
python3 -m pip install --upgrade pip setuptools wheel && \
pip install -r requirements.txt && \
python -m playwright install chromium && \
pip install -e . && \
net-scan --version
```

#### Ubuntu/Debian (with specific Python 3.11)

```bash
# Update package lists
sudo apt-get update

# Install required system libraries
sudo apt-get install -y python3-dev libxml2-dev libxslt1-dev zlib1g-dev build-essential
```

#### Fedora/RHEL/CentOS

```bash
# Install required system libraries
sudo dnf install -y python3-devel libxml2-devel libxslt-devel zlib-devel gcc
```

#### macOS

```bash
# Install using Homebrew
brew install libxml2 libxslt

# If you don't have Homebrew installed, download from https://brew.sh
```

#### Alpine Linux

```bash
# Install required system libraries
apk add --no-cache python3-dev libxml2-dev libxslt-dev zlib-dev
```

### Verify Python Installation

**Windows (PowerShell):**
```powershell
python --version
```

**Linux/macOS (Bash):**
```bash
python3 --version
```

**Expected output:** `Python 3.11.0` or higher

If Python is not installed, download from [python.org](https://www.python.org/downloads/) and ensure "Add Python to PATH" is checked during installation.

---

## Installation

### Step 1: Download or Clone Repository

```powershell
# Windows
cd C:\Users\YourName\Desktop
git clone https://github.com/alfredsimeon/net_scan.git
cd net-scan

# Or if you don't have git, extract the ZIP file and navigate to it
```

```bash
# Linux/macOS
cd ~
git clone https://github.com/alfredsimeon/net_scan.git
cd net-scan
```

### Step 2: Create Virtual Environment

**Virtual environments isolate NET_SCAN dependencies and prevent pip issues. Highly recommended!**

#### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\\venv\\Scripts\\Activate.ps1

# If you get an execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux/macOS (Bash)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**You should see `(venv)` at the start of your terminal prompt after activation.**

---

## Setup & Activation

### Complete Installation

#### Windows (PowerShell)

```powershell
# Make sure you're in the project directory and venv is activated
# (you should see (venv) in your prompt)

# Upgrade pip
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (required for JavaScript rendering)
python -m playwright install

# Install NET_SCAN in development mode
pip install -e .
```

#### Linux/macOS (Bash)

```bash
# Make sure you're in the project directory and venv is activated
# (you should see (venv) in your prompt)

# Upgrade pip
python3 -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (required for JavaScript rendering)
python -m playwright install

# Install NET_SCAN in development mode
pip install -e .
```

**Note:** The Playwright installation downloads browser binaries (~500MB) and may take a few minutes.

### Using Virtual Environment Later

Every time you want to use NET_SCAN, activate the virtual environment:

**Windows:**
```powershell
.\\venv\\Scripts\\Activate.ps1
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

To exit the virtual environment:
```bash
deactivate
```

---

## Verification

After installation, verify everything works:

```bash
# Check NET_SCAN version
net-scan --version

# Check configuration
net-scan config

# View all available commands
net-scan --help
```

All three commands should complete without errors.

---

## Usage Walkthrough

### Basic Scan (5 minutes)

```bash
# Make sure venv is activated first!
net-scan scan scanme.nmap.org --profile quick
```

This performs a quick vulnerability assessment with basic tests only.

### Recommended Scan (15 minutes)

```bash
# This is the default balanced profile
net-scan scan scanme.nmap.org
```

This performs comprehensive testing across all vulnerability types.

### Aggressive Scan (45+ minutes)

```bash
# Extensive testing with advanced techniques
net-scan scan scanme.nmap.org --profile aggressive
```

This performs the most thorough scan with all available tests.

### Specific Vulnerability Tests

```bash
# Test only SQL Injection, XSS, and CSRF
net-scan scan scanme.nmap.org --tests sqli,xss,csrf
```

Available test types: `sqli`, `xss`, `csrf`, `cmd_injection`, `path_traversal`, `xxe`, `ssrf`

### Custom Crawl Depth and Pages

```bash
# Crawl 5 levels deep, test up to 200 pages
net-scan scan scanme.nmap.org --depth 5 --max-pages 200
```

### With Burp Suite or OWASP ZAP Proxy

```bash
# Route all traffic through Burp Suite
net-scan scan scanme.nmap.org --proxy http://localhost:8080
```

Useful for:
- Logging all requests in Burp
- Modifying requests on-the-fly
- Inspecting scanner behavior

### Interactive Mode

```bash
# Interactive menu for custom scanning
net-scan interactive
```

Allows you to:
- Select targets
- Choose vulnerability tests
- Customize parameters
- Run scans step-by-step

### Generate Multiple Report Formats

```bash
# Generate HTML, JSON, and Markdown reports
net-scan scan scanme.nmap.org --report html,json,markdown
```

### Custom Threads

```bash
# Use 20 threads for faster scanning (be careful not to overload servers)
net-scan scan scanme.nmap.org --threads 20
```

### Dry Run (Preview without testing)

```bash
# Shows what would be scanned without actually testing
net-scan scan scanme.nmap.org --dry-run
```

---

## Scan Profiles

NET_SCAN provides three built-in scan profiles:

### Quick Profile (~5 minutes)
```bash
net-scan scan scanme.nmap.org --profile quick
```
- **Crawl depth:** 2 levels
- **Max pages:** 30
- **Tests:** SQLi and XSS only
- **Best for:** Initial reconnaissance

### Balanced Profile (~15 minutes - Default)
```bash
net-scan scan scanme.nmap.org
# or explicitly: net-scan scan scanme.nmap.org --profile balanced
```
- **Crawl depth:** 3 levels
- **Max pages:** 100
- **Tests:** All 7 vulnerability types
- **Best for:** Standard security assessments (recommended)

### Aggressive Profile (~45+ minutes)
```bash
net-scan scan scanme.nmap.org --profile aggressive
```
- **Crawl depth:** 5 levels
- **Max pages:** 500
- **Tests:** All vulnerability types with advanced techniques
- **Best for:** Comprehensive deep security audits

---

## Advanced Configuration

### Custom Payloads

Edit `net_scan/utils/payloads.py` to customize:
- SQL injection payloads
- XSS test vectors
- Command injection patterns
- Path traversal attempts
- XXE and SSRF probes

### Timeout Configuration

```bash
# Increase timeout to 60 seconds
net-scan scan scanme.nmap.org --timeout 60
```

Default: 10 seconds

### Multiple Threads

```bash
# Use 15 concurrent threads (caution: may impact target server)
net-scan scan scanme.nmap.org --threads 15
```

Default: 5 threads

### Output Directory

Reports are generated in the `reports/` directory by default.

### Logging

Check `logs/net_scan.log` for detailed execution logs.

---

## Report Output

### Report Types Generated

After each scan, three reports are automatically generated in the `reports/` directory:

#### 1. HTML Report (`reports/report_[timestamp].html`)
- **Best for:** Visual review and stakeholder presentations
- **Features:**
  - Interactive charts and severity breakdown
  - Color-coded vulnerability levels
  - Clickable findings with details
  - Remediation steps
  - Evidence and proof of concept
  - Professional layout

#### 2. JSON Report (`reports/report_[timestamp].json`)
- **Best for:** Automation, CI/CD integration, and data processing
- **Features:**
  - Machine-readable format
  - Complete metadata
  - All findings with parameters
  - Payload information
  - CVSS scores
  - Easy integration with other tools

#### 3. Markdown Report (`reports/report_[timestamp].md`)
- **Best for:** Version control, documentation, and sharing
- **Features:**
  - Plain text format
  - Git-friendly
  - Easy to share via email
  - Print-friendly
  - Good for documentation

### Report Content

All reports include:
- **Executive Summary** - High-level overview with severity counts
- **Vulnerability Findings** - Detailed information for each issue including:
  - Vulnerability type and location (URL + parameter)
  - Payload used for detection
  - CVSS v3.1 score
  - Evidence showing the vulnerability
  - Detailed explanation
  - Remediation recommendations
  - Security best practices
  - OWASP and CWE references
- **Scan Statistics** - Pages crawled, tests performed, time taken
- **Remediation Workflow** - Step-by-step fix guidance

### Severity Levels

| Level | CVSS Score | Action |
|-------|-----------|---------|
| **CRITICAL** | 9.0-10.0 | Requires immediate remediation |
| **HIGH** | 7.0-8.9 | Should be addressed urgently |
| **MEDIUM** | 4.0-6.9 | Should be remediated soon |
| **LOW** | 0.1-3.9 | Lower risk, but should address |

### Example Finding

```json
{
  "type": "SQL Injection",
  "location": "https://target.com/search?q=test",
  "parameter": "q",
  "method": "GET",
  "severity": "CRITICAL",
  "cvss_score": 8.6,
  "payload": "1' AND SLEEP(5)--",
  "evidence": "Response time increased from 0.12s to 5.45s",
  "remediation": "Use parameterized queries or prepared statements"
}
```

---

## Troubleshooting

### Issue: Virtual Environment Activation Fails

**Error:** `cannot be loaded because running scripts is disabled`

**Solution (Windows):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry activation with `.\\venv\\Scripts\\Activate.ps1`

### Issue: "pip: command not found"

**Solution 1 (Recommended):** Use Python module syntax
```powershell
# Windows
python -m pip install -r requirements.txt

# Linux/macOS
python3 -m pip install -r requirements.txt
```

**Solution 2:** Ensure virtual environment is activated
- Windows: You should see `(venv)` in your PowerShell prompt
- Linux/macOS: You should see `(venv)` in your bash prompt

If not activated, run:
- Windows: `.\\venv\\Scripts\\Activate.ps1`
- Linux/macOS: `source venv/bin/activate`

**Solution 3:** Reinstall pip
```powershell
# Windows
python -m ensurepip --upgrade

# Linux/macOS
python3 -m ensurepip --upgrade
```

### Issue: "net-scan: command not found"

**Cause:** NET_SCAN not installed or virtual environment not active

**Solution:**
```bash
# Activate venv first
.\\venv\\Scripts\\Activate.ps1      # Windows
source venv/bin/activate            # Linux/macOS

# Reinstall NET_SCAN
pip install -e .
```

### Issue: "Playwright browsers not found"

**Solution (Kali Linux):**
```bash
# Install all system dependencies with apt
sudo apt install -y chromium-browser chromium libnss3 libnspr4 libx11-6 libxext6 \
  libxrender1 libxrandr2 libgbm1 libdrm2 libdbus-1-3 libexpat1 libssl3 libcups2 libpulse0

# Then install Playwright browser
python -m playwright install chromium
```

This may take a few minutes and download ~500MB of browser binaries.

**Verify JavaScript rendering works:**
```bash
python -c "
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://example.com')
        title = await page.title()
        print(f'✅ JavaScript rendering works: {title}')
        await browser.close()

asyncio.run(test())
"
```

### Issue: Timeout Errors

**Solution:** Increase the timeout value
```bash
net-scan scan scanme.nmap.org --timeout 60
```

Default is 10 seconds. Increase for slow servers.

### Issue: "Module not found" errors

**Cause:** Dependencies not properly installed or wrong Python environment

**Solution:**
```bash
# Ensure venv is activated
# Then reinstall dependencies
pip install -r requirements.txt
python -m playwright install
pip install -e .
```

### Issue: Proxy Connection Errors

**Solution:** Verify your proxy is running and accessible
```bash
# Test proxy connectivity
# For Burp: http://localhost:8080
# For OWASP ZAP: http://localhost:8080
# For other proxies: Use your actual proxy URL and port

# Then retry
net-scan scan scanme.nmap.org --proxy http://localhost:8080
```

### Issue: JavaScript Not Rendering

**Cause:** Playwright browsers not properly installed

**Solution:**
```bash
# Reinstall Playwright browsers
python -m playwright install chromium
```

### Issue: Slow Scanning Performance

**Solutions:**
1. Use `--profile quick` for initial scans
2. Reduce `--max-pages` (try 50-100 instead of default)
3. Adjust `--depth` based on URL structure
4. Increase `--threads` carefully (monitor server load)

---

## Architecture

```
net-scan/
├── net_scan/
│   ├── __init__.py                 # Package initialization
│   ├── cli.py                      # Click CLI interface (150 lines)
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── crawler.py              # Web crawler with JS rendering (350 lines)
│   │   ├── engine.py               # Scanning orchestrator (250 lines)
│   │   └── detectors/              # Vulnerability detection modules
│   │       ├── __init__.py
│   │       ├── sql_injection.py    # SQL injection (200 lines)
│   │       ├── xss.py              # XSS detection (150 lines)
│   │       ├── csrf.py             # CSRF detection (100 lines)
│   │       ├── cmd_injection.py    # Command injection (120 lines)
│   │       └── advanced.py         # XXE, SSRF, Path traversal (200 lines)
│   ├── report/
│   │   ├── __init__.py
│   │   └── generator.py            # Multi-format report generation (500 lines)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py               # Security logging (80 lines)
│   │   ├── terminal_ui.py          # Retro terminal UI (200 lines)
│   │   ├── http_client.py          # Async HTTP client (250 lines)
│   │   └── payloads.py             # Payload generation (300 lines)
│   ├── config/                     # Scan profiles & configuration
│   └── db/                         # Findings database
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Python dependencies (17 packages)
├── README.md                       # This file
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore rules
```

### Technology Stack

- **Python 3.11+** - Async-native with type hints throughout
- **Playwright** - JavaScript-capable web crawling with headless Chrome
- **asyncio + aiohttp** - Concurrent HTTP testing with connection pooling
- **BeautifulSoup4 + lxml** - HTML/XML parsing
- **Click** - Professional CLI framework
- **Jinja2** - HTML report template generation
- **SQLAlchemy** - Database ORM
- **cryptography** - Secure data handling
- **pydantic** - Data validation
- **rich** - Enhanced terminal output
- **colorama** - Cross-platform colored text

---

## Security & Legal

### ⚠️ Important Legal Notice

**NET_SCAN should ONLY be used on systems you own or have explicit written permission to test.**

Unauthorized access to computer systems is illegal under the:
- Computer Fraud and Abuse Act (CFAA) in the US
- Computer Misuse Act in the UK
- Similar laws in other jurisdictions

### Before Using NET_SCAN

1. **Obtain Written Authorization** - Get explicit permission from the system owner
2. **Define Scope** - Clearly specify which systems can be tested
3. **Establish Timeline** - Agree on testing dates and times
4. **Inform IT Teams** - Notify infrastructure teams to prevent false alarms
5. **Use Isolated Environment** - Test on non-production systems first

### Best Practices

- Always use `--dry-run` first to preview targets
- Test on systems you control before testing others
- Proxy all traffic through your own test infrastructure
- Review findings carefully; some may require manual verification
- Keep detailed logs and reports for compliance
- Use appropriate authentication for authorized access
- Respect rate limiting and server resources

### Compliance

- OWASP Top 10 coverage
- CVSS v3.1 severity scoring
- GDPR-compliant data handling
- Designed for authorized penetration testing

---

## About

### Developer

**Fred (alfredsimeon)**
- Creator and Maintainer of NET_SCAN
- GitHub: https://github.com/alfredsimeon
- Repository: https://github.com/alfredsimeon/net_scan

### License

MIT License - See LICENSE file for details

You are free to:
- ✅ Use for authorized security testing
- ✅ Modify and customize
- ✅ Distribute and integrate
- ✅ Use commercially (with proper authorization of test targets)

### Support & Contributions

- **Issues & Features:** Report on GitHub: https://github.com/alfredsimeon/net_scan/issues
- **Questions:** Contact via GitHub profile
- **Contributions:** Pull requests welcome!

### Disclaimer

This tool is provided "as is" without warranty. The author is not responsible for:
- Unauthorized use of this tool
- Damage caused by misuse
- Legal consequences of unauthorized access
- False positives or false negatives in findings

---

**Last Updated:** January 2026  
**Version:** 1.0.0  
**Status:** Production-Ready
