#!usr/bin/env python3
import logging

from .__fancytable import FancyTable
from .__formatters import TableFormatter

logger = logging.getLogger(__name__)

__version__ = "0.1a2"


logger.info("fancytables is alive! v" + __version__)
