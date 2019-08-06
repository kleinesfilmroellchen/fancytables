.. fancytables documentation master file, created by
   sphinx-quickstart on Tue Jul 30 20:08:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fancytables's documentation!
=======================================

.. toctree::
    :glob:
    :maxdepth: 2
    :caption: Contents:

    api/*

API design and basic usage information
--------------------------------------

The fancytables package is separated into the parts *data* and *output*.
While :class:`fancytables.FancyTable` is responsible for accumulating,
accessing and organizing data, this class and its subclasses handle
outputting and formatting this data. This also means that this class can
never be used by itself and always operates on instances of FancyTable.

The separation of data and format means the following:

- :class:`fancytables.FancyTable`'s formatting methods always delegate to this class's implementations and their methods.
- :class:`fancytables.FancyTable` does know about options that affect formatting, but only if these options further affect data processing. This currently affects the header's ``content`` property, which defines content type and is used for type checking.
- :class:`fancytables.FancyTable` does know about very specific abstract options that affect single columns. This currently affects the header's ``important`` property, which will only affect formatting but cannot be determined by the formatting class.
- :class:`fancytables.TableFormatter` does not know about data; it only gets to know about the table at formatting time and queries it for its data.

These methods allow for the usual duck-typing:

1. As long as the object allows double indexing, has a ``headers`` property
    and supports ``len()``, it is accepted as a data-providing table by a
    formatter.
2. As long as the object is callable with one argument and returns a string,
    it can be used on methods that take in a table formatter.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
