import os
import sys

from loguru import logger as log

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

log.remove(0)
log.add(
    sys.stderr,
    level=LOG_LEVEL,
    format=(
        '\033[1;33m{time:YYYY-MM-DD-TZ at HH:mm:ss}\033[1;37m'
        ' [line {line} in {file}] \033[1;36m{level}\033[1;32m ~ {message}'
    ),
    catch=True,
    backtrace=False,
    diagnose=False,
    colorize=True,
)
