# PPLG.__init__.py
# CodeWriter21

__version__ = "1.0.1"
__author__ = "CodeWriter21 (Mehrad Pooryoussof)"
__github__ = "Https://GitHub.com/MPCodeWriter21/PyPassListGen"

from PPLG.lib import Generate
from PPLG.lib.Generate import *


def entry_point():
    from PPLG.__main__ import main, logger
    try:
        main()
    except KeyboardInterrupt:
        logger.error('\033[91mKeyboardInterrupt: Cancelled!')
