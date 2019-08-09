.. py:module:: fancytables

Table formatting
================

The TableFormatter class
------------------------

.. autoclass:: fancytables.TableFormatter
   :members:


.. autofunction:: fancytables.TableFormatter.__call__

.. _built-in:

Built-in implementations of table formatting
--------------------------------------------

The package provides several builtin implementations of table formatting that
can be used for simple use cases where quick access to a standard formatter is
necessary.

.. autoproperty:: fancytables.TableFormatter.Unicode

.. autoproperty:: fancytables.TableFormatter.Ascii

.. autoproperty:: fancytables.TableFormatter.Borderless

.. _extending:

Extending TableFormatter
------------------------

The recommended way of writing your own table formatter is by extending the
:class:`fancytables.TableFormatter` base class and overriding some of its
methods. There are three different ways of providing formatting capabilities,
which have to do with how the :func:`fancytables.TableFormatter.__call__`
method works:

#. All formatting invokes the object like a method, which triggers the
   ``__call__`` method. To this method is passed the table to be formatted.
   Although further arguments could be specified, they are useless because the
   package's builtin mechanisms for formatting only pass one argument, as
   stated. The method is expected to return a string that represents the full
   table in formatted fashion, with possibly many newlines ``\n`` to separate
   lines. If you want to have full control over all formatting, you can
   override the call method or instead simply use a one-argument function as a
   formatter (the formatting mechanisms apply usual pythonic duck-typing). For
   most use cases, though, this is way too tedious, as you probably have to
   implement most of the formatting mechanisms all over again. Therefore, the
   advice is to only override the ``__call__`` method or use plain functions in
   special cases where extremely advanced and specific formatting is required.
#. The ``__call__`` method will check the different formatting sub-methods,
   whose structure and desired behavior is listed above. This whole process
   is called the **Formatting Algorithm**. On an abstract (but still fully
   comprehensive) level, it works like this:

    #. Check if the method :func:`fancytables.TableFormatter.column_format`
       returns something else than ``NotImplemented``. If so, format every
       column using this method and stick them together correctly. Return the
       result.
    #. Check if the method :func:`fancytables.TableFormatter.row_format`
       returns something else than ``NotImplemented``. If so, format every
       row, including a pseudo-row containing the headers, using this method
       and stick them together correctly. Return the result.
    #. Check if the method :func:`fancytables.TableFormatter.get_border`
       returns something else than ``NotImplemented``. If so:

        #. Check if the method :func:`fancytables.TableFormatter.cell_format`
           returns something else than ``NotImplemented``. If so, format every
           cell using this method and stick them together with simple space
           left/right padding and the borders returned by the ``get_border``
           method. If not, use default formatting for the cells instead.
        #. Check if the method :func:`fancytables.TableFormatter.header_format`
           returns something else than ``NotImplemented``. If so, format every
           header (cell) using this method and stick them together with simple
           space left/right padding and the borders returned by the
           ``get_border`` method. If not, use default formatting for the
           headers instead.

    #. Invoke the default :class:`fancytables.TableFormatter.Unicode`
       formatter, because this formatter does not provide a single
       comprehensive formatting mechanism.

As the ``get_border`` method is a great way of providing borders with different
directions, you are encouraged to implement and use it even if you work with
the :func:`fancytables.TableFormatter.column_format` or
:func:`fancytables.TableFormatter.row_format` methods.

One additional piece of information needs to be provided regarding the
header(s) that are passed into various functions. They include the full
header data from the table, but also more formatting-related information;
for this reason, they are called **Formatter Headers**.

* **width** The width a header's column content (and the header itself) has
   to have as determined by the column contents. The
   :func:`fancytables.TableFormatter.cell_format` method should always return a
   string of this precise size.

See the source code of ``__call__`` for advanced and detailed information
about the formatting algorithm:

.. TODO: use correct line numbers

.. literalinclude:: ../../fancytables/__formatters.py
    :linenos:
    :language: python
    :lines: 34-50
