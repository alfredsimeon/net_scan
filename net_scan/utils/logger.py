"""
NET_SCAN - Logging and configuration module
Provides centralized logging with security best practices
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

class SecurityLogger:
    """Production-grade logger with sensitive data redaction"""
    
    def __init__(self, name: str, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # File handler - rotate logs
        log_file = self.log_dir / f"net_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(detailed_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def redact_sensitive(self, text: str) -> str:
        """Redact sensitive data like passwords, tokens, keys"""
        import re
        
        patterns = {
            r'(?i)(password|passwd|pwd|secret)\s*[=:]\s*[\'"]?([^\s\'"]+)': r'\1=***REDACTED***',
            r'(?i)(token|api[_-]?key|auth)\s*[=:]\s*[\'"]?([^\s\'"]+)': r'\1=***REDACTED***',
            r'(?i)(cookie|session)\s*[=:]\s*[\'"]?([^\s\'"]+)': r'\1=***REDACTED***',
        }
        
        redacted = text
        for pattern, replacement in patterns.items():
            redacted = re.sub(pattern, replacement, redacted)
        return redacted
    
    def info(self, message: str):
        self.logger.info(self.redact_sensitive(message))
    
    def debug(self, message: str):
        self.logger.debug(self.redact_sensitive(message))
    
    def warning(self, message: str):
        self.logger.warning(self.redact_sensitive(message))
    
    def error(self, message: str, exc_info: bool = False):
        self.logger.error(self.redact_sensitive(message), exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        self.logger.critical(self.redact_sensitive(message), exc_info=exc_info)

# Global logger instance
logger = SecurityLogger("NET_SCAN")
