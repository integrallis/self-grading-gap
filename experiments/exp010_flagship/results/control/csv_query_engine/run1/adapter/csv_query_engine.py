# file: csv_query_engine.py
from candidate import count as _count
from candidate import filter as _filter
from candidate import limit as _limit
from candidate import order as _order
from candidate import project as _project
from candidate import read_csv as _read_csv

UnknownColumnError = ValueError


class CsvQuery:
    def __init__(self, csv_text):
        self._records = _read_csv(csv_text)

    @classmethod
    def _from_records(cls, records):
        query = cls.__new__(cls)
        query._records = records
        return query

    def count(self):
        return _count(self._records)

    def keys(self):
        return next(iter(self._records)).keys()

    def limit(self, n):
        return self._from_records(_limit(self._records, n))

    def order_by(self, column, direction='asc'):
        return self._from_records(_order(self._records, column, direction))

    def rows(self):
        return self._records

    def select(self, *columns):
        return self._from_records(_project(self._records, columns))

    def where(self, column, operator, value):
        return self._from_records(_filter(self._records, column, operator, value))
