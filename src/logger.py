import logging
from datetime import datetime

class Colors:
    
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'

class ColoredFormatter(logging.Formatter):
    
    COLORS = {
        'DEBUG': Colors.BRIGHT_BLUE,
        'INFO': Colors.BRIGHT_GREEN,
        'WARNING': Colors.BRIGHT_YELLOW,
        'ERROR': Colors.BRIGHT_RED,
        'CRITICAL': Colors.BRIGHT_MAGENTA
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Colors.RESET}"

        if levelname in self.COLORS:
            record.msg = f"{self.COLORS[levelname]}{record.msg}{Colors.RESET}"
        
        return super().format(record)

def setup_logger():
    logger = logging.getLogger('taberna_logger')
    logger.setLevel(logging.INFO)
    
    log_filename = f"logs/taberna_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
 
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger() 