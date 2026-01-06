"""NET_SCAN package initialization"""

__version__ = "1.0.0"
__author__ = "Fred (alfredsimeon)"
__author_url__ = "https://github.com/alfredsimeon"
__repository__ = "https://github.com/alfredsimeon/net_scan"
__license__ = "MIT"

from net_scan.utils.logger import logger
from net_scan.utils.terminal_ui import TerminalUI

__all__ = ["logger", "TerminalUI"]
