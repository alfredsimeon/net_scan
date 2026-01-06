# NET_SCAN - Quick Start Guide

## Installation

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd net-scan

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (required for JavaScript rendering)
playwright install

# Install NET_SCAN
pip install -e .
```

### Step 2: Verify Installation

```bash
net-scan --version
net-scan config
```

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
