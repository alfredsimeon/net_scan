# NET_SCAN - Quick Start Guide

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

**Verify Python Installation:**

**Windows:**
```powershell
python --version
```

**Linux/macOS:**
```bash
python3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

---

### Step 1: Create Virtual Environment

**Recommended Approach:** Using Python's built-in venv for isolated environment setup

#### Windows Setup

```powershell
# Navigate to project directory
cd net-scan

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\\venv\\Scripts\\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Once activated, you should see `(venv)` at the start of your terminal prompt.

#### Linux/macOS Setup

```bash
# Navigate to project directory
cd net-scan

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

Once activated, you should see `(venv)` at the start of your terminal prompt.

---

### Step 2: Install Python Dependencies

**After activating the virtual environment:**

#### Windows

```powershell
# Upgrade pip (important for compatibility)
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (required for JavaScript rendering)
python -m playwright install

# Install NET_SCAN in development mode
pip install -e .
```

#### Linux/macOS

```bash
# Upgrade pip (important for compatibility)
python3 -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (required for JavaScript rendering)
python -m playwright install

# Install NET_SCAN in development mode
pip install -e .
```

---

### Step 3: Verify Installation

```bash
net-scan --version
net-scan config
```

If commands are not found, ensure the virtual environment is activated (you should see `(venv)` in your prompt).

---

### Troubleshooting pip Issues

#### Issue: "pip: command not found" or "pip is not recognized"

**Solution 1: Use Python module syntax (Recommended)**

```powershell
# Windows
python -m pip install -r requirements.txt

# Linux/macOS
python3 -m pip install -r requirements.txt
```

**Solution 2: Ensure virtual environment is activated**

- Windows: You should see `(venv)` in your PowerShell prompt
- Linux/macOS: You should see `(venv)` in your bash prompt

If not activated, run:
- Windows: `.\\venv\\Scripts\\Activate.ps1`
- Linux/macOS: `source venv/bin/activate`

**Solution 3: Reinstall pip in virtual environment**

```bash
# Windows
python -m ensurepip --upgrade

# Linux/macOS
python3 -m ensurepip --upgrade
```

#### Issue: "Module not found" or import errors after installation

**Solution:** Make sure you're in the correct virtual environment

```bash
# Check active Python interpreter
which python          # Linux/macOS
which python.exe      # Windows with Git Bash

# Should show path inside venv/ directory
```

---

### Deactivating Virtual Environment

When done working:

```bash
deactivate
```

This returns you to your system Python environment.

## Basic Usage

### Quick Scan (5 minutes)

```bash
net-scan scan https://target.com --profile quick
```

### Balanced Scan (15 minutes - Recommended)

```bash
net-scan scan https://target.com
```

### Aggressive Scan (45+ minutes)

```bash
net-scan scan https://target.com --profile aggressive
```

## Advanced Usage

### Scan with Burp Suite Proxy

```bash
net-scan scan https://target.com --proxy http://localhost:8080
```

### Scan Specific Vulnerability Types

```bash
net-scan scan https://target.com --tests sqli,xss,csrf
```

### Custom Crawl Depth and Pages

```bash
net-scan scan https://target.com --depth 5 --max-pages 200
```

### Interactive Mode

```bash
net-scan interactive
```

## Report Formats

NET_SCAN generates three types of reports automatically:

1. **HTML Report** - Visual, browser-viewable with charts and colors
2. **JSON Report** - Machine-readable for automation and integration
3. **Markdown Report** - Version-control friendly text format

All reports include:
- Executive summary with severity breakdown
- Detailed findings with evidence
- CVSS scoring for each vulnerability
- Remediation recommendations with implementation steps
- Security references and best practices

Reports are saved in the `reports/` directory by default.

## Understanding Results

### Severity Levels

| Level | CVSS Score | Definition |
|-------|-----------|-----------|
| **CRITICAL** | 9.0-10.0 | Requires immediate remediation |
| **HIGH** | 7.0-8.9 | Should be addressed urgently |
| **MEDIUM** | 4.0-6.9 | Should be remediated soon |
| **LOW** | 0.1-3.9 | Lower risk impact |

### Example: SQL Injection Finding

```
[CRITICAL] SQL Injection (Time-based)
  URL: https://target.com/search?q=test
  Parameter: q
  Payload: 1' AND SLEEP(5)--
  CVSS Score: 8.6
  Evidence: Response time increased from 0.12s to 5.45s
```

## Remediation Workflow

1. **Review Findings** - Open the HTML report in your browser
2. **Prioritize by Severity** - Start with CRITICAL and HIGH vulnerabilities
3. **Implement Fixes** - Follow the remediation steps in the report
4. **Re-scan** - Run NET_SCAN again to verify the fixes
5. **Document** - Keep reports for compliance and historical tracking

## Troubleshooting

### "Playwright browsers not found"

```bash
playwright install
```

### Timeout Errors

Increase the timeout value:
```bash
net-scan scan https://target.com --timeout 60
```

### Proxy Connection Issues

Ensure your proxy (Burp, ZAP) is running on the specified port:
```bash
net-scan scan https://target.com --proxy http://localhost:8080
```

### JavaScript Not Rendering

The scanner uses headless Chrome. Ensure Playwright is properly installed:
```bash
playwright install chromium
```

## Performance Tips

1. **Use `--profile quick`** for initial reconnaissance
2. **Reduce `--max-pages`** for large sites (try 50-100)
3. **Adjust `--depth`** based on URL structure
4. **Use `--threads`** to balance speed vs. system load

## Security Best Practices

✓ **DO:**
- Obtain written authorization before scanning
- Test on staging environments first
- Review findings with security team
- Keep scan reports for compliance
- Update NET_SCAN regularly

✗ **DON'T:**
- Scan without explicit permission
- Use on production systems without preparation
- Share scan results without need-to-know
- Ignore remediation recommendations
- Disable security features for speed

## Support & Contributing

For issues, feature requests, or contributions:
1. Check the main README.md
2. Review existing vulnerabilities and detectors
3. Test thoroughly before deployment

## Next Steps

1. **Run a test scan** on your application
2. **Review the HTML report** in detail
3. **Implement remediation** recommendations
4. **Re-run scanner** to verify fixes
5. **Integrate into CI/CD** for continuous security

---

**Created by:** Fred (alfredsimeon)
**GitHub Repository:** https://github.com/alfredsimeon/net_scan
**Author Profile:** https://github.com/alfredsimeon

**Remember:** This tool is for authorized security testing only. Always respect laws and obtain proper authorization.
