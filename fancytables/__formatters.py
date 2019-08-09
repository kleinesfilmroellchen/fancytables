#!usr/bin/env python3
import logging
from copy import deepcopy
from typing import List
from itertools import chain

from .__const import default_formatter_header

logger = logging.getLogger(__package__)


class TableFormatter:
    """
    Base class of table formatting.

    This class does not do anything by itself, but provides the structure for
    real formatters. It is strongly recommended for all table formatters to be
    a subclass of this class (although of course, duck typing allows for
    exceptions).

    See :ref:`extending` for more information on how to write your own
    table formatter.

    :param inverted: Whether to invert the table when it is passed in. As the
                     inversion is processed in __call__ and not the real
                     formatting methods, it takes effect for all children that
                     do not override the __call__ method.
    :param align:    How to align ALL columns: left "l", right "r" or center
                     "c". This option must be processed by the children.
    """

    def __init__(self, inverted: bool = False, align: str = None):
        self.inverted = inverted
        self.align = align

    def __call__(self, table):
        """
        Calling a TableFormatter is the main way of using its formatting
        capabilities. Subclasses are strongly discouraged from overwriting
        this method, as it handles invoking different format specification
        methods depending on their definition. See :ref:`extending` for more
        details.

        If this method is overwritten, it allows full customization of the
        formatting, which will probably be too tedious for most applications.
        """
        # logger.debug("Formatter call invoked")
        # warning: this is python at its finest, be prepared to be amazed of
        # how terrible I use all of this language's amazing features

        # prepare minimum width
        # oh fuck yes python this is awesome
        min_widths = map(lambda elts:
                         (lambda header, *col:
                          TableFormatter.determine_width(
                              chain((header['title']), col))
                          )(*elts),  # use hack to spread arguments with nested lambda
                         # zip headers and data transposed
                         zip(table.headers, *table.data)
                         )
        # logger.debug(" ".join(map(lambda x: str(x), min_widths)))

        cf = self.column_format(
            [], default_formatter_header, 0)
        if cf is not NotImplemented:
            logger.debug("Using column format method")

            def column_creator(args):
                # logger.debug(args)
                orig_header, min_width, *col = args
                # logger.debug("%s %s %s", str(orig_header),
                #              str(min_width), str(col))
                header = deepcopy(orig_header)
                header['width'] = min_width
                pos = -1 if table.headers.index(orig_header) == 0 else \
                    1 if table.headers.index(orig_header) == len(table.headers) - 1 \
                    else 0
                return self.column_format(col, header, pos)

            column_list = map(column_creator, zip(
                table.headers, min_widths, *table.data))

            # logger.debug(list(column_list))
            return "\n".join(("".join(tup) for tup in zip(*column_list)))

        rf = self.row_format([], default_formatter_header)
        if rf is not NotImplemented:
            # use row format method
            logger.debug("Using row format method")

            def formatter_headers():
                nonlocal min_widths
                for header, min_width in zip(table.headers, min_widths):
                    header['width'] = min_width
                    yield header

            row_list = map(
                lambda row: self.row_format(row, formatter_headers()),
                chain(deepcopy(table.headers), table.data))
            return "\n".join(row_list)

    def get_border(self, top: bool = False, right: bool = False, bottom: bool = False, left: bool = False) -> str:
        """
        One of the basic method of specifing table formatting. This method
        should provide a single character string that represents the table
        border with a connection to the given sides. Any side is marked as
        having a connection if its corresponding argument value is set to True
        (or a truthy value). By default, there is no connection to any side and
        this method should return the space character ``' '`` in such a case.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def cell_format(self, header: dict, content) -> str:
        """
        Define how a single cell WITHOUT PADDING AND SEPARATORS should be
        formatted. This is a simple and encouraged way of dealing with custom
        cell formatting.

        :param header: The *Formatter Header* dictionary.

        :param content: The cell contents to be formatted, can be any datatype.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def header_format(self, header: dict) -> str:
        """
        Define how a header WITHOUT PADDING AND BORDERS should be formatted.

        :param header: The *Formatter Header* dictionary.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def column_format(self, column: list, column_header: dict, pos: int) -> List[str]:
        """
        Define how an entire column should be formatted. This method should
        return a list of strings which represents the text lines that this
        column is made out of. The header needs to be included in the output.
        As this method's results are simply 'glued together', this method
        should include padding and borders.

        :param column: The list of elements in this column.
        :param column_header: The *Formatter Header* dictionary.
        :param pos: The position of the column: -1 if first column, 0 if middle column, 1 if last
                    column. Use this to determine which borders to draw (e.g. left and right
                    borders if first column, only right border for all others).

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def row_format(self, row: list, headers: List[dict]) -> str:
        '''
        Define how an entire row should be formatted. This method should
        return a string without a trailing newline which represents this row.
        As this method's results are simply 'glued together', this method
        should include padding and borders.

        :param row: The list of elements in this row.
        :param headers: All *Formatter Header* s of the table.

        '''
        return NotImplemented

    @staticmethod
    def determine_width(column: iter) -> int:
        maxelmt = max(map(lambda x: str(x), column), key=len)
        # logger.debug("Largest element from " +
        #              str(column) + " is " + str(maxelmt))
        return len(maxelmt)


        # ----------------------------------------
        # standard implementations go here
        # TODO: implement unicode formatter
TableFormatter.Unicode = TableFormatter()
TableFormatter.Unicode.__doc__ = """Standard formatter implementation, which is also the
default for quick formatting methods such as :func:`fancytables.FancyTable.__format__`"""

# TODO: implement ascii formatter
TableFormatter.Ascii = TableFormatter()
TableFormatter.Ascii.__doc__ = """MySQL - like formatter which only uses
ASCII characters; therefore, this formatter is recommended if your project has
issues with Unicode. This formatter can be enabled with python's new-style
formatting, see :func:`fancytables.FancyTable.__format__` for more information."""

# TODO: implement borderless formatter
TableFormatter.Borderless = TableFormatter()
TableFormatter.Borderless.__doc__ = """Simple borderless table formatter.
This also capitalizes headers, which makes it akin to many command-line table
outputs found in \\*nix system commands. This formatter can be enabled with
python's new-style formatting, see :func:`fancytables.FancyTable.__format__`
for more information."""


del List
