#!usr/bin/env python3
from typing import List
import logging
logger = logging.getLogger(__package__)


class TableFormatter:
    """
    Base class of table formatting.

    This class does not do anything by itself, but provides the structure for
    real formatters. It is strongly recommended for all table formatters to be
    a subclass of this class (although of course, duck typing allows for
    exceptions)

    See :ref:`extending` for more information on how to write your own
    table formatter
    """

    def __init__(self, inverted=False, **kwargs):
        self.inverted = inverted

    def __call__(self, *args, **kwargs):
        """
        Calling a TableFormatter is the main way of using its formatting
        capabilities. Subclasses are strongly discouraged from overwriting
        this method, as it handles invoking different format specification
        methods depending on their definition. See :ref:`extending` for more
        details.

        If this method is overwritten, it allows full customization of the
        formatting, which will probably be too tedious for most applications.
        """

    def get_border(self, top: bool = False, right: bool = False, bottom: bool = False, left: bool = False) -> str:
        """
        One of the basic method of specifing table formatting. This method
        should provide a single character string that represents the table
        border with a connection to the given sides. Any side is marked as
        having a connection if its corresponding argument value is set to True
        (or a truthy value). By default, there is no connection to any side and
        this method should return an empty string in such a case.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def cell_format(self, header: dict, content, width: int) -> str:
        """
        Define how a single cell WITHOUT PADDING AND SEPARATORS should be
        formatted. This is a simple and encouraged way of dealing with custom
        cell formatting.

        :param header: The header information dictionary, as given to the
                       FancyTable through the :func:`fancytables.FancyTable.headers` property.

        :param content: The cell contents to be formatted, can be any datatype.

        :param width: The width this content has to have as determined
                      by the column contents. This means that this method should always
                      return a string which has this precise size.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def header_format(self, header: dict, width: int) -> str:
        """
        Define how a header should be formatted. Returns a string that has the
        header information formatted to be used in the final table string.

        :param header: The header information dictionary, as given to the
                       FancyTable through the :func:`fancytables.FancyTable.headers` property.

        :param width: The width this header's CONTENT has to have as determined
                      by the column contents. This means that this method should always
                      return a string whose content portion (excluding the vertical
                      separators and spacing) has this precise size.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented

    def column_format(self, column_header: dict, min_width: int) -> List[str]:
        """
        Define how an entire column should be formatted. This method should
        return a list of strings which represents the text lines that this
        column is made out of.

        :param column_header: The header information dictionary, as given to the
                              FancyTable through the :func:`fancytables.FancyTable.headers` property.

        :param min_width: The width this column's CONTENT has to have as
                          determined by the column contents. This means that this method should
                          always return a string whose content portion (excluding the vertical
                          separators and spacing) has *at least* this precise size.

        If this method returns ``NotImplemented``, it is not used in formatting
        . Subclasses should use this behavior to instead provide other
        formatting providing methods.
        """
        return NotImplemented


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
