#!usr/bin/env python3
import copy
from itertools import islice
import logging
from typing import List
from numbers import Number

from .__formatters import TableFormatter

logger = logging.getLogger(__package__)


class FancyTable:
    """
    The FancyTable class holds table data and can output formatted text tables.

    Table output is possible in four different ways:

    - Using the pseudo-property :prop:`fancytables.FancyTable.formatted`. This will
      always return a normally formatted Unicode table without special borders,
      order or text format. Example: ::
        ft = FancyTable()
        # insert data...
        str(ft.formatted) # will return a basic formatted table

    - Using new-style formatting (``str.format()``) with custom arguments that
      can determine basic formatting options. Example: ::
        ft = FancyTable()
        # insert data...
        "{:...options go here...}".format(ft)

    See :func:`fancytables.FancyTable().__format__` for information about formatting options.

    - Using the method ``format_table()`` with

        a. the ``TableFormatter``, whose constructor allows the basic levels of
        format customization. Instead, the TableFormatter constructor arguments
        can also be directly passed to the ``format_table()`` method.

        b. a ``TableFormatter`` subclass, either one of the built-in classes or
        user-defined classes.
        This allows for the highest level of customization, but is the most tedious
        on the user side.

    The usual way of adding rows to the table is by using ``+``. For
    information on the data that can be added, see the
    :class:`fancytables.FancyTable.__add__` method documentation. This allows
    for very intuitive data addition, such as: ::
        ft = FancyTable('a','b','c')
        ft += ['foo', 'bar', 'baz']     # add one row
        ft += [4, 5, 6]                 # and another one
        ft += [['some', 'str', 'list'],
               ['mo', 're', 'lists']]   # add two rows at once
        feces = ft + ['poop', '💩', '💩'] # copy table with additional rows

    Init arguments:

    :param headers: A list which defines this table's headers. Note that only
        data which aligns with a header is regarded, i.e. rows that are longer
        than a header only have the first n elements added, where n is the
        header count. E.g. if the headers are ``["a", "b", "c"]``,
        then from the row ``[1, 2, 3, 4, 5]``, only 1, 2 and 3 will be added.
        Each header entry can either be:

            a. a string, which will lead to default column options when printing.
            b. a dict-like, which allows you to define abstract options that
               affect formatting and printing. Possible keys are:
                - **title** (str): define the header title.
                - **content** (callable): define the header type. This is done
                  by using a callable that takes one argument (the value to be
                  used) and returns the converted value. It can throw a
                  ``ValueError`` to indicate a bad value

    :param data: Initial data to be inserted into the table. See
        :class:`fancytables.FancyTable.__add__` for information on possible
        data
    """

    def __init__(self, headers: list = None, data: iter = None):
        self.__headers = self.__parse_headers(
            headers if headers is not None else [])
        self.__data = self.__parse_data(
            self.__headers, data if data is not None else [])
        # logger.debug(str(self.__data) + str(self.__headers))

    def __format__(self, format_spec):
        """
        Returns the formatted text table with basic options passed through
        the ``format_spec`` option. This method is automatically called when a
        FancyTables object is used with new-style formatting, such as
        ``"{:}".format(FancyTables())``. The string between the curly brackets
        after the colon is passed to this method as the format_spec argument.

        Possible options (in this exact order, none mandatory):

            - Alignment: use well-known alignment operators directly after ':'
              to left-justify (<), right-justify (>) or center (^) ALL columns.
            - Minimum column width: use well-known width specifier by means of
              a positive integer to specify minimum width that ALL columns
              should have. If a column exceeds this lower limit, it will be
              made wider. Use zero (0) to indicate arbitrary column width
              (default).
            - Table style: Basic Unicode table style is used by default. Use
              'a' to force basic ASCII table style or 'b' to force basic
              borderless table style.
        """
        logger.debug("Called format with args " + format_spec)
        return str(self)

    def __str__(self):
        # other arguments go here...
        return self.__class__.__name__ + "("  # + ")"

    def __bytes__(self):
        return bytes(str(self), "utf-8")

    @property
    def formatted(self):
        """
        Returns the formatted text table with standard options and unicode
        characters.
        """
        # call formatter
        return TableFormatter.Unicode(self)

    def format_table(self, formatter, **kwargs):
        """
        Format the table using a certain formatter.

        This method will always call the formatter, therefore a callable or a
        TableFormatter instance needs to be passed.
        """
        if formatter is None:
            logger.debug(
                "No formatter passed, using keyword arguments " + str(kwargs))

    @staticmethod
    def __parse_headers(headers):
        """Utility method to change all entries in the headers list into a dict."""
        # mapper function for headers
        def mapheader(header):
            try:
                return dict(header)
            except ValueError:
                return {"title": str(header),
                        "content": "generic",
                        "important": False}
            return None

        return list(filter(lambda x: x is not None,
                           map(mapheader, headers)))

    @staticmethod
    def __parse_data(headers: dict, data: iter) -> List[list]:
        if len(data) == 0:
            return []
        try:
            # try making an iterator out of all elements except strings
            # if that doesn't throw a single error, we have a nested iterator
            lst = [iter(elmt) if type(elmt) is not str else elmt
                   for elmt in data]
            # logger.debug("Nested iterator: " + str(lst))
            retlist = []
            for element in lst:
                try:
                    retlist.append(
                        FancyTable.__parse_innerdata(headers, element))
                except TypeError:
                    # occurs when inner part of the method (see below) fails
                    pass
            return retlist
        except TypeError:
            # only if no fully nested iterable is provided
            return [FancyTable.__parse_innerdata(headers, data)]

    @staticmethod
    def __parse_innerdata(headers: dict, data: iter) -> list:
        retlist = []
        for header, val in zip(headers, data):
            retlist.append(FancyTable.typecheck_data(header["content"], val))
        return retlist

    @staticmethod
    def typecheck_data(header_type, value):
        '''
        Typechecks the given value with the given header type. This method
        accounts for the special 'generic' type as well as the other 'stringy'
        types that need to be given for the builtin types. The reason for not
        simply using the builtin type callables such as int, bool, float etc.
        is that they will accept a wide range of values that are clearly not
        of the correct type. E.g. ``bool('a') => True`` ('a' is not wanted as
        an entry to a boolean column). Therefore, these types are handled
        separately by this method as they are passed as strings, not as
        callables.
        '''
        if type(header_type) is str:
            retval = {'int': (lambda i: int(i) if isinstance(i, Number) and not isinstance(i, complex) else NotImplemented),
                      'float': (lambda f: float(f) if isinstance(f, Number) and not isinstance(f, complex) else NotImplemented),
                      'generic': (lambda s: str(s)), 'str': (lambda s: str(s)),
                      'bool': (lambda b: b if b is True or b is False else NotImplemented),
                      'list': (lambda l: list(l) if isinstance(l, List) else NotImplemented),
                      'dict': (lambda d: dict(d) if isinstance(d, dict) else NotImplemented),
                      }[header_type](value)
            if retval is NotImplemented:
                raise TypeError(
                    'Incorrect datatype: "' + str(value) + '" should be '
                    + str(header_type))
            return retval
        else:
            try:
                return header_type(value)
            except ValueError:
                raise TypeError(
                    'Incorrect datatype: "' + str(value) + '" should be '
                    + str(header_type))

    @property
    def headers(self):
        """
        Modify or lookup the table headers. **Attention: Once you access the table
        headers, a copy is created. Modifications on such an object will not
        affect the original headers!**
        """
        return self.__headers.copy()

    @headers.setter
    def headers(self, headers):
        self.__headers = self.__parse_headers(headers)
        logger.debug(self.__headers)

    @headers.deleter
    def headers(self):
        self.__headers = []

    @property
    def data(self):
        """
        Property for retrieving, overriding or deleting all of the table's
        data. The data retrieved is always deeply copied (see
        `copy.deepcopy() <https://docs.python.org/library/copy.html#copy.deepcopy>`_)
        """
        return copy.deepcopy(self.__data.copy())

    @data.setter
    def data(self, data):
        self.__data = self.__parse_data(self.__headers, data)

    @data.deleter
    def data(self):
        self.__data = []

    def __add__(self, other):
        """Add table content to this FancyTable. This is the main way of adding
        new content to the FancyTable and supports many different content types:

        - A single list or iterable (not **only** nested with other lists) is regarded
          as one row of data, and the elements correspond to the headers in order.
          Excess elements are ignored, so infinite iterators can be passed
          to this method.
        - A nested list or iterable (the only contents of the iterable are other
          iterables) is treated as several rows that are to be added. In this
          case, the outer iterable must not be infinite, as this method attempts
          to fully consume it.

        This method throws a :class:`TypeError` if any of the columns have a
        fixed datatype and a given value for that column does not match the
        column type. If nested iterables (see above) are given, all the
        rows before the one where the error occured are still added.
        """
        newtable = copy.deepcopy(self)
        try:
            newtable.__data.extend(
                FancyTable.__parse_data(self.headers, other))
        except TypeError as te:
            raise te
        return newtable

    def __sub__(self, other):
        newtable = copy.deepcopy(self)
        newtable.__data = newtable.__data[:-int(other)]
        return newtable
