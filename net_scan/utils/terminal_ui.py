"""
NET_SCAN - Terminal UI module
Vintage retro terminal aesthetic with animations
"""

import sys
import time
from typing import Optional
from colorama import Fore, Back, Style, init

init(autoreset=True)

class TerminalUI:
    """Retro terminal UI with ASCII art and animations"""
    
    @staticmethod
    def print_banner():
        """Print NET_SCAN banner with vintage aesthetic"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                           {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}███╗   ██╗███████╗████████╗    ███████╗ ██████╗ █████╗ ██╗   ██╗{Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}████╗  ██║██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝{Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}██╔██╗ ██║█████╗     ██║       ███████╗██║     ███████║ ╚████╔╝ {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}██║╚██╗██║██╔══╝     ██║       ╚════██║██║     ██╔══██║  ╚██╔╝  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}██║ ╚████║███████╗   ██║       ███████║╚██████╗██║  ██║   ██║   {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.GREEN}╚═╝  ╚═══╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                           {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}        {Fore.YELLOW}Production-Grade Web Vulnerability Scanner{Fore.CYAN}      ║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                    {Fore.YELLOW}v1.0.0{Fore.CYAN}                         ║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                           {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    @staticmethod
    def print_typing_text(text: str, speed: float = 0.02):
        """Animated typing effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()
    
    @staticmethod
    def print_section(title: str):
        """Print section header"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}▶ {title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    @staticmethod
    def print_status(message: str, status: str = "INFO"):
        """Print status message with color coding"""
        colors = {
            "INFO": Fore.BLUE,
            "SUCCESS": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.RED + Back.BLACK,
        }
        color = colors.get(status, Fore.WHITE)
        symbol = {
            "INFO": "[i]",
            "SUCCESS": "[+]",
            "WARNING": "[!]",
            "ERROR": "[-]",
            "CRITICAL": "[!]",
        }.get(status, "[*]")
        
        print(f"{color}{symbol} {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_progress_bar(current: int, total: int, prefix: str = "", length: int = 40):
        """Print animated progress bar"""
        # Handle edge case: no items to test
        if total == 0:
            print(f"\r{prefix} {Fore.YELLOW}[No testable endpoints found]{Style.RESET_ALL}", end="")
            print()
            return
        
        # Calculate progress percentage and filled bar
        percent = 100 * (current / float(total))
        filled = int(length * current // total)
        bar = "█" * filled + "░" * (length - filled)
        
        print(f"\r{prefix} {Fore.CYAN}[{bar}]{Style.RESET_ALL} {percent:.1f}%", end="")
        if current == total:
            print()
    
    @staticmethod
    def print_vulnerability(vuln: dict):
        """Pretty print vulnerability finding"""
        severity_colors = {
            "CRITICAL": Fore.RED + Style.BRIGHT,
            "HIGH": Fore.RED,
            "MEDIUM": Fore.YELLOW,
            "LOW": Fore.GREEN,
            "INFO": Fore.BLUE,
        }
        
        color = severity_colors.get(vuln.get("severity", "INFO"), Fore.WHITE)
        
        print(f"\n{color}{'─'*60}{Style.RESET_ALL}")
        print(f"{color}[{vuln.get('severity', 'UNKNOWN')}]{Style.RESET_ALL} {vuln.get('type', 'Unknown')}")
        print(f"  {Fore.CYAN}URL:{Style.RESET_ALL} {vuln.get('url', 'N/A')}")
        print(f"  {Fore.CYAN}Parameter:{Style.RESET_ALL} {vuln.get('parameter', 'N/A')}")
        print(f"  {Fore.CYAN}CVSS Score:{Style.RESET_ALL} {vuln.get('cvss_score', 'N/A')}")
        if vuln.get('description'):
            print(f"  {Fore.CYAN}Description:{Style.RESET_ALL} {vuln.get('description')}")
    
    @staticmethod
    def print_table(data: list, headers: list):
        """Print ASCII table"""
        if not data:
            print("No data to display")
            return
        
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in data:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(f"{h:<{w}}" for h, w in zip(headers, widths))
        print(f"\n{Fore.CYAN}{header_row}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * len(header_row)}{Style.RESET_ALL}")
        
        # Print data rows
        for row in data:
            print(" | ".join(f"{str(cell):<{w}}" for cell, w in zip(row, widths)))
    
    @staticmethod
    def spinner(duration: float = 1.0):
        """Animated spinner"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        start = time.time()
        i = 0
        
        while time.time() - start < duration:
            sys.stdout.write(f"\r{Fore.CYAN}{frames[i % len(frames)]}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write("\r")
        sys.stdout.flush()
