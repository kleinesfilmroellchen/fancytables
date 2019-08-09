#!usr/bin/env python3

from itertools import islice

from .__fancytable import FancyTable
from .__formatters import TableFormatter


def basic_example():
    """
    Basic example code demonstrating very simple use cases of FancyTable.
    """

    table = FancyTable(headers=["City name", "Area",
                                "Population", "Annual Rainfall"])

    table += ["Adelaide", 1295, 1158259, 600.5]
    table += ["Brisbane", 5905, 1857594, 1146.4]
    table += ["Darwin", 112, 120900, 1714.7]
    table += ["Hobart", 1357, 205556, 619.5]
    table += ["Sydney", 2058, 4336374, 1214.8]
    table += ["Melbourne", 1566, 3806092, 646.9]
    table += ["Perth", 5386, 1554769, 869.4]

    print(table.formatted)


def make_exampletable():
    """Returns an example FancyTable filled with example city data. Use this
    to try out the formatting options."""

    # insert data directly as 2d array
    return FancyTable(headers=["City name", "Area",
                               "Population", "Annual Rainfall"],
                      data=[["Adelaide", 1295, 1158259, 600.5],
                            ["Brisbane", 5905, 1857594, 1146.4],
                            ["Darwin", 112, 120900, 1714.7],
                            ["Hobart", 1357, 205556, 619.5],
                            ["Sydney", 2058, 4336374, 1214.8],
                            ["Melbourne", 1566, 3806092, 646.9],
                            ["Perth", 5386, 1554769, 869.4]])


def example_customformatter():
    table = make_exampletable()
    print(table.formatted)
    formatter = TableFormatter()

    formatter.column_format = \
        lambda column, header, minwidth, pos: \
        [(f'X {{:{str(minwidth)}}} X').format(header['title'])] + \
        [(f'# {{:{str(minwidth)}}} #').format(cell) for cell in column]
    print(formatter(table))


def example_dataadding():
    """
    Example of different ways of adding data to a FancyTable.
    """
    table = make_exampletable()
    print(table.formatted)
    # ---------------------------------------------------------------
    # add new data as 2d list
    table = FancyTable(headers=["City name", "Area",
                                "Population", "Annual Rainfall"])
    table += [["Adelaide", 1295, 1158259, 600.5],
              ["Brisbane", 5905, 1857594, 1146.4],
              ["Darwin", 112, 120900, 1714.7],
              ["Hobart", 1357, 205556, 619.5],
              ["Sydney", 2058, 4336374, 1214.8],
              ["Melbourne", 1566, 3806092, 646.9],
              ["Perth", 5386, 1554769, 869.4]]
    # can be done multiple times
    table += [["Timbuktu", 928, 0, 1.6],
              ["My home town", 341, 43280, 958.6]]
    print(table.formatted)
    # ---------------------------------------------------------------
    # add new data from an iterator
    table = FancyTable(headers=["City name", "Area",
                                "Population", "Annual Rainfall"])
    table += islice(city_simulator(), 20)
    table += islice(city_simulator(), 3)
    print(table.formatted)
    # remove some data
    table -= 5
    print(table.formatted)


def example_from_database():
    """
    Example of reading data from a
    `DB-API 2.0 <https://www.python.org/dev/peps/pep-0249/>`_
    database into a FancyTable. SQLite 3 is used for simplicity.
    """
    # setup simple sqlite3 in-memory database
    from sqlite3 import connect
    conn = connect(":memory:")
    conn.executescript("""create table cities (
                                name varchar(20) primary key,
                                area integer,
                                population integer,
                                rainfall float);
                            insert into cities (name, area, population, rainfall)
                                values (("Adelaide", 1295, 1158259, 600.5),
                                    ("Brisbane", 5905, 1857594, 1146.4),
                                    ("Darwin", 112, 120900, 1714.7),
                                    ("Hobart", 1357, 205556, 619.5),
                                    ("Sydney", 2058, 4336374, 1214.8),
                                    ("Melbourne", 1566, 3806092, 646.9),
                                    ("Perth", 5386, 1554769, 869.4)
                                );""")
    conn.commit()
    # these two lines is all the code necessary for reading the data.
    table = FancyTable(headers=["City name", "Area",
                                "Population", "Annual Rainfall"])
    table.add_from_db(db=conn, table="cities")
    print(table.formatted)
    print(make_exampletable().formatted)


def city_simulator():
    from random import Random
    r = Random()
    cityname = [x for x in "meiamacityohiamsobeautifuljustimaginethislol"]
    while True:
        r.shuffle(cityname)
        yield ["".join(cityname)[:r.randint(7, 15)], abs(r.gauss(3000, 4000)), abs(r.gauss(100_000, 30_000)), r.gauss(700.0, 150.0)]


del islice
