#!usr/bin/env python3


class FancyTable:

    """
    The FancyTable class is the base class of the package.
    It holds table data and can output formatted text tables.

    Table output is possible in four different ways:

    - Using the pseudo-property `.formatted`. This will
      always return a normally formatted Unicode table without special borders,
      order or text format. Example:


    ```python
    ft = FancyTable()
    # insert data...
    str(fancytable) # will return a basic formatted table
    ```


    - Using new-style formatting (`str.format()`) with custom arguments that
     can determine basic formatting options. Example:


    ```python
    ft = FancyTable()
    # insert data...
    "{:...options go here...}".format(ft)
    ```


    See the `FancyTable.__format__()` Documentation for information about formatting options.


    - Using the method `format_table()` with
        a) the `TableFormatter`, whose constructor allows the basic levels of
        format customization. Instead, the TableFormatter constructor arguments
        can also be directly passed to the `format_table()` method.
        b) a `TableFormatter` subclass, either one of the built-in classes or
        user-defined classes.
        This allows for the highest level of customization, but is the most tedious
        on the user side.


    """

    def __init__(self, **kwargs):
        pass

    def __format__(self, format_spec):
        """
        Returns the formatted text table with basic options passed through
        the `format_spec` option. This method is automatically called when a
        FancyTables object is used with new-style formatting, such as
        `"{:}".format(FancyTables())`. The string between the curly brackets
        after the colon is passed to this method as the format_spec argument.

        Possible options:


        """
        print("Called format with args", format_spec)
        return str(self)

    def __str__(self):
        # other arguments go here... + + ")"
        return self.__class__.__name__ + "("

    def __bytes__(self):
        return bytes(str(self), "utf-8")

    @property
    def formatted(self):
        """
        Returns the formatted text table with standard options and unicode
        characters.
        """
        # call formatter
        return ""
