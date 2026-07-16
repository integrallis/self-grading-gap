# file: csv_query_engine.py
from candidate import count as _count
from candidate import filter as _filter
from candidate import limit as _limit
from candidate import order as _order
from candidate import project as _project
from candidate import read_csv as _read_csv

UnknownColumnError = ValueError


class CsvQuery:
    raises = staticmethod(UnknownColumnError)

    def __init__(self, csv_text):
        self._records = _read_csv(csv_text)

    def select(self, *columns):
        self._records = _project(self._records, columns)
        return self

    def where(self, column, operator, value):
        self._records = _filter(self._records, column, operator, value)
        return self

    def order_by(self, column, direction="asc"):
        self._records = _order(self._records, column, direction)
        return self

    def limit(self, count):
        self._records = _limit(self._records, count)
        return self

    def rows(self):
        return self._records

    def count(self):
        return _count(self._records)

    def keys(self):
        return next(iter(self._records), {}).keys()
