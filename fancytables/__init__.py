#!usr/bin/env python3
from .__fancytable import FancyTable
from .__formatters import TableFormatter
import logging
logger = logging.getLogger(__name__)

__version__ = "0.1a2"


logger.info("prettytables is alive! v" + __version__)
