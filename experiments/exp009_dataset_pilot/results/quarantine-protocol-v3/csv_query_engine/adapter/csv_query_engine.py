# file: csv_query_engine.py
from candidate.impl import CSVQueryEngine as CsvQuery

UnknownColumnError = ValueError

CsvQuery.rows = CsvQuery.materialize
