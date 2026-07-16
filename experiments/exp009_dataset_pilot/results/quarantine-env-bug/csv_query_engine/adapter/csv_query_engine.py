# file: csv_query_engine.py
from candidate.impl import CSVQueryEngine as _CSVQueryEngine
from candidate.impl import ValueError as _ValueError

class UnknownColumnError(Exception):
    pass

class CsvQuery:
    def __init__(self, csv_text):
        self.engine = _CSVQueryEngine(csv_text)

    def select(self, *columns):
        self.engine.select(*columns)
        return self

    def where(self, column, operator, value):
        try:
            self.engine.where(column, operator, value)
        except ValueError as e:
            if "Unknown column" in str(e):
                raise UnknownColumnError(str(e))
            raise
        return self

    def order_by(self, column, direction):
        self.engine.order_by(column, direction)
        return self

    def limit(self, count):
        self.engine.limit(count)
        return self

    def count(self):
        return self.engine.count()

    def execute(self):
        return self.engine.execute()
