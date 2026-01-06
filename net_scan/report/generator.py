"""
NET_SCAN - Report Generator
Professional vulnerability reports with remediation recommendations
"""

from typing import List, Dict, Optional
from datetime import datetime
import json
import logging
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)

class CVSSCalculator:
    """CVSS v3.1 score calculation"""
    
    SEVERITY_RANGES = {
        (0.0, 0.0): ("NONE", "gray"),
        (0.1, 3.9): ("LOW", "green"),
        (4.0, 6.9): ("MEDIUM", "yellow"),
        (7.0, 8.9): ("HIGH", "red"),
        (9.0, 10.0): ("CRITICAL", "darkred"),
    }
    
    @staticmethod
    def get_severity(score: float) -> tuple:
        """Get severity level from CVSS score"""
        for (min_score, max_score), (level, color) in CVSSCalculator.SEVERITY_RANGES.items():
            if min_score <= score <= max_score:
                return level, color
        return "UNKNOWN", "white"
    
    @staticmethod
    def calculate_custom_score(
        vulnerability_type: str,
        exploitability: float = 0.8,
        impact: float = 0.8
    ) -> float:
        """Calculate custom CVSS-like score"""
        base_scores = {
            'SQL Injection': 8.6,
            'Cross-Site Scripting': 7.5,
            'CSRF': 6.5,
            'OS Command Injection': 9.8,
            'Path Traversal': 7.5,
            'XXE': 8.1,
            'SSRF': 7.8,
        }
        
        return base_scores.get(vulnerability_type, 6.5)

class RemediationRecommendations:
    """Security recommendations for each vulnerability type"""
    
    RECOMMENDATIONS = {
        'SQL Injection': {
            'description': 'Attackers can execute arbitrary SQL commands, leading to unauthorized data access, modification, or deletion.',
            'steps': [
                'Use parameterized queries (prepared statements) for all database operations',
                'Implement input validation and whitelisting for all user inputs',
                'Use ORM frameworks that automatically handle parameterization',
                'Escape special SQL characters when input validation is not sufficient',
                'Apply principle of least privilege to database accounts',
                'Use Web Application Firewall (WAF) rules to detect SQL injection patterns',
            ],
            'references': [
                'OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection',
                'OWASP Top 10 2021 - A03:2021 Injection',
            ],
            'priority': 'CRITICAL'
        },
        'Cross-Site Scripting': {
            'description': 'Attackers can inject malicious scripts that execute in users\' browsers, stealing cookies, sessions, or performing actions on behalf of users.',
            'steps': [
                'Encode all user input based on context (HTML, JavaScript, URL, CSS)',
                'Use Content Security Policy (CSP) headers to restrict script execution',
                'Implement input validation and output encoding',
                'Use security-focused templating engines that auto-encode by default',
                'Sanitize HTML input using libraries like DOMPurify or bleach',
                'Regularly update and patch client-side dependencies',
            ],
            'references': [
                'OWASP XSS Prevention Cheat Sheet',
                'OWASP Top 10 2021 - A03:2021 Injection',
            ],
            'priority': 'HIGH'
        },
        'CSRF': {
            'description': 'Attackers can trick authenticated users into performing unwanted actions on other websites.',
            'steps': [
                'Implement CSRF tokens for all state-changing requests',
                'Use SameSite cookie attribute (Strict or Lax)',
                'Verify Origin and Referer headers',
                'Use POST instead of GET for sensitive operations',
                'Implement double-submit cookie pattern as backup',
                'Use framework built-in CSRF protection mechanisms',
            ],
            'references': [
                'OWASP CSRF Prevention Cheat Sheet',
                'SameSite Cookie Explained: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite',
            ],
            'priority': 'MEDIUM'
        },
        'OS Command Injection': {
            'description': 'Attackers can execute arbitrary system commands on the server, potentially compromising the entire system.',
            'steps': [
                'Avoid using shell execution functions (exec, system, passthru)',
                'Use library functions that don\'t invoke shells when available',
                'Implement strict input validation and whitelist allowed commands',
                'Use parameterized system calls',
                'Run application with minimal necessary privileges',
                'Disable unnecessary system functions in PHP/other languages',
            ],
            'references': [
                'OWASP Command Injection: https://owasp.org/www-community/attacks/Command_Injection',
                'CWE-78: OS Command Injection',
            ],
            'priority': 'CRITICAL'
        },
        'Path Traversal': {
            'description': 'Attackers can access files outside the intended directory, potentially exposing sensitive system files.',
            'steps': [
                'Canonicalize file paths and check against allowed directory',
                'Use whitelisting for allowed file paths',
                'Avoid user input in file paths when possible',
                'Use secure file path handling libraries',
                'Implement proper file access controls and permissions',
                'Run application with minimal file system access',
            ],
            'references': [
                'OWASP Path Traversal: https://owasp.org/www-community/attacks/Path_Traversal',
                'CWE-22: Improper Limitation of a Pathname to a Restricted Directory',
            ],
            'priority': 'MEDIUM'
        },
    }
    
    @staticmethod
    def get_recommendations(vuln_type: str) -> Dict:
        """Get remediation recommendations for vulnerability type"""
        return RemediationRecommendations.RECOMMENDATIONS.get(
            vuln_type,
            {
                'description': 'A security vulnerability has been detected.',
                'steps': [
                    'Review security best practices',
                    'Implement input validation',
                    'Apply security patches',
                ],
                'references': ['OWASP Top 10'],
                'priority': 'MEDIUM'
            }
        )

class ReportGenerator:
    """Generate security reports in multiple formats"""
    
    def __init__(self, findings: List[Dict], target_url: str):
        self.findings = findings
        self.target_url = target_url
        self.scan_date = datetime.now()
        self.severity_counts = self._count_by_severity()
    
    def _count_by_severity(self) -> Dict[str, int]:
        """Count findings by severity"""
        counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'INFO': 0,
        }
        
        for finding in self.findings:
            severity = finding.get('severity', 'INFO')
            if severity in counts:
                counts[severity] += 1
        
        return counts
    
    def generate_html(self, output_file: str) -> str:
        """Generate HTML report"""
        logger.info(f"Generating HTML report to {output_file}")
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NET_SCAN Security Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .metadata {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        
        .metadata-item {{
            background: #161b22;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #388bfd;
        }}
        
        .metadata-item label {{
            color: #7d8590;
            font-size: 0.9em;
            display: block;
            margin-bottom: 5px;
        }}
        
        .severity-summary {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px;
            margin: 30px 0;
        }}
        
        .severity-box {{
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            color: white;
        }}
        
        .severity-critical {{ background: #da3633; }}
        .severity-high {{ background: #f85149; }}
        .severity-medium {{ background: #fbca04; color: black; }}
        .severity-low {{ background: #1f6feb; }}
        .severity-info {{ background: #6e40aa; }}
        
        .severity-box .count {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .severity-box .label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .section {{
            background: #161b22;
            padding: 25px;
            border-radius: 5px;
            margin-bottom: 25px;
            border: 1px solid #30363d;
        }}
        
        h2 {{
            color: #79c0ff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #30363d;
        }}
        
        .finding {{
            background: #0d1117;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 5px;
            border-left: 4px solid #388bfd;
        }}
        
        .finding.critical {{ border-left-color: #da3633; }}
        .finding.high {{ border-left-color: #f85149; }}
        .finding.medium {{ border-left-color: #fbca04; }}
        .finding.low {{ border-left-color: #1f6feb; }}
        
        .finding-type {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #79c0ff;
        }}
        
        .finding-details {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin: 15px 0;
            font-size: 0.95em;
        }}
        
        .finding-detail {{
            background: #161b22;
            padding: 10px;
            border-radius: 3px;
        }}
        
        .finding-detail label {{
            color: #7d8590;
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        
        .payload {{
            background: #0d1117;
            padding: 10px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            border: 1px solid #30363d;
            margin: 10px 0;
        }}
        
        .remediation {{
            background: #0d1117;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        
        .remediation h4 {{
            color: #79c0ff;
            margin-bottom: 10px;
        }}
        
        .remediation ol {{
            margin-left: 20px;
        }}
        
        .remediation li {{
            margin-bottom: 8px;
        }}
        
        .reference {{
            color: #58a6ff;
            text-decoration: none;
            font-size: 0.9em;
        }}
        
        .reference:hover {{
            text-decoration: underline;
        }}
        
        footer {{
            text-align: center;
            padding: 20px;
            color: #7d8590;
            border-top: 1px solid #30363d;
            margin-top: 40px;
        }}
        
        .no-findings {{
            color: #7d8590;
            text-align: center;
            padding: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ NET_SCAN Security Report</h1>
            <p>Production-Grade Vulnerability Assessment</p>
        </header>
        
        <div class="metadata">
            <div class="metadata-item">
                <label>Target URL</label>
                <strong>{self.target_url}</strong>
            </div>
            <div class="metadata-item">
                <label>Scan Date</label>
                <strong>{self.scan_date.strftime('%Y-%m-%d %H:%M:%S')}</strong>
            </div>
            <div class="metadata-item">
                <label>Total Findings</label>
                <strong>{len(self.findings)}</strong>
            </div>
        </div>
        
        <div class="severity-summary">
            <div class="severity-box severity-critical">
                <div class="count">{self.severity_counts['CRITICAL']}</div>
                <div class="label">CRITICAL</div>
            </div>
            <div class="severity-box severity-high">
                <div class="count">{self.severity_counts['HIGH']}</div>
                <div class="label">HIGH</div>
            </div>
            <div class="severity-box severity-medium">
                <div class="count">{self.severity_counts['MEDIUM']}</div>
                <div class="label">MEDIUM</div>
            </div>
            <div class="severity-box severity-low">
                <div class="count">{self.severity_counts['LOW']}</div>
                <div class="label">LOW</div>
            </div>
            <div class="severity-box severity-info">
                <div class="count">{self.severity_counts['INFO']}</div>
                <div class="label">INFO</div>
            </div>
        </div>
        
        <div class="section">
            <h2>Executive Summary</h2>
            <p>
                This security assessment identified <strong>{len(self.findings)}</strong> vulnerabilities across the target application.
                The following severity breakdown was recorded:
            </p>
            <ul style="margin-left: 20px; margin-top: 15px;">
                <li><strong>Critical:</strong> {self.severity_counts['CRITICAL']} findings that require immediate remediation</li>
                <li><strong>High:</strong> {self.severity_counts['HIGH']} findings that should be addressed urgently</li>
                <li><strong>Medium:</strong> {self.severity_counts['MEDIUM']} findings that should be remediated soon</li>
                <li><strong>Low:</strong> {self.severity_counts['LOW']} findings with lower risk impact</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>Detailed Findings</h2>
"""
        
        if not self.findings:
            html += '<div class="no-findings"><p>✓ No vulnerabilities detected</p></div>'
        else:
            for i, finding in enumerate(self.findings, 1):
                severity = finding.get('severity', 'INFO').lower()
                html += f"""
            <div class="finding {severity}">
                <div class="finding-type">#{i} {finding.get('type', 'Unknown')} [{finding.get('severity', 'INFO')}]</div>
                <div class="finding-details">
                    <div class="finding-detail">
                        <label>URL</label>
                        {finding.get('url', 'N/A')}
                    </div>
                    <div class="finding-detail">
                        <label>Parameter</label>
                        {finding.get('parameter', 'N/A')}
                    </div>
                    <div class="finding-detail">
                        <label>Method</label>
                        {finding.get('method', 'N/A')}
                    </div>
                    <div class="finding-detail">
                        <label>CVSS Score</label>
                        {finding.get('cvss_score', 'N/A')}
                    </div>
                </div>
                
                <div class="remediation">
                    <h4>Remediation Recommendations</h4>
                    {self._generate_remediation_html(finding)}
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <footer>
            <p>NET_SCAN v1.0.0 | Security Assessment Tool</p>
            <p>Report generated automatically. Review findings with your security team.</p>
        </footer>
    </div>
</body>
</html>
"""
        
        # Write to file with UTF-8 encoding (required for Unicode characters on Windows)
        Path(output_file).write_text(html, encoding='utf-8')
        logger.info(f"HTML report saved to {output_file}")
        return output_file
    
    def generate_json(self, output_file: str) -> str:
        """Generate JSON report"""
        logger.info(f"Generating JSON report to {output_file}")
        
        report = {
            'scan_info': {
                'target_url': self.target_url,
                'scan_date': self.scan_date.isoformat(),
                'total_findings': len(self.findings),
                'severity_summary': self.severity_counts,
            },
            'findings': self.findings,
        }
        
        Path(output_file).write_text(json.dumps(report, indent=2), encoding='utf-8')
        logger.info(f"JSON report saved to {output_file}")
        return output_file
    
    def generate_markdown(self, output_file: str) -> str:
        """Generate Markdown report"""
        logger.info(f"Generating Markdown report to {output_file}")
        
        md = f"""# NET_SCAN Security Assessment Report

## Executive Summary

- **Target:** {self.target_url}
- **Scan Date:** {self.scan_date.strftime('%Y-%m-%d %H:%M:%S')}
- **Total Findings:** {len(self.findings)}

### Severity Breakdown

| Severity | Count |
|----------|-------|
| CRITICAL | {self.severity_counts['CRITICAL']} |
| HIGH | {self.severity_counts['HIGH']} |
| MEDIUM | {self.severity_counts['MEDIUM']} |
| LOW | {self.severity_counts['LOW']} |
| INFO | {self.severity_counts['INFO']} |

## Detailed Findings

"""
        
        if not self.findings:
            md += "✓ No vulnerabilities detected\n"
        else:
            for i, finding in enumerate(self.findings, 1):
                md += f"""### {i}. {finding.get('type', 'Unknown')} [{finding.get('severity', 'INFO')}]

- **URL:** {finding.get('url', 'N/A')}
- **Parameter:** {finding.get('parameter', 'N/A')}
- **Method:** {finding.get('method', 'N/A')}
- **CVSS Score:** {finding.get('cvss_score', 'N/A')}

**Evidence:** {finding.get('evidence', 'N/A')}

{self._generate_remediation_md(finding)}

---

"""
        
        Path(output_file).write_text(md, encoding='utf-8')
        logger.info(f"Markdown report saved to {output_file}")
        return output_file
    
    def _generate_remediation_html(self, finding: Dict) -> str:
        """Generate HTML remediation section"""
        vuln_type = finding.get('type', 'Unknown')
        recommendations = RemediationRecommendations.get_recommendations(vuln_type)
        
        html = f"""<p>{recommendations.get('description', '')}</p>
                    <strong>Remediation Steps:</strong>
                    <ol>"""
        
        for step in recommendations.get('steps', []):
            html += f"<li>{step}</li>"
        
        html += """</ol><strong>References:</strong><ul>"""
        
        for ref in recommendations.get('references', []):
            if ref.startswith('http'):
                html += f'<li><a href="{ref}" class="reference" target="_blank">{ref}</a></li>'
            else:
                html += f'<li>{ref}</li>'
        
        html += """</ul>"""
        
        return html
    
    def _generate_remediation_md(self, finding: Dict) -> str:
        """Generate Markdown remediation section"""
        vuln_type = finding.get('type', 'Unknown')
        recommendations = RemediationRecommendations.get_recommendations(vuln_type)
        
        md = f"""#### Remediation

{recommendations.get('description', '')}

**Steps to Fix:**
"""
        
        for step in recommendations.get('steps', []):
            md += f"1. {step}\n"
        
        md += "\n**References:**\n"
        for ref in recommendations.get('references', []):
            md += f"- {ref}\n"
        
        return md
