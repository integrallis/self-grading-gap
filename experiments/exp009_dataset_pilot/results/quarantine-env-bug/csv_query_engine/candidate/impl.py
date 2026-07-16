import csv
import re

class CSVQueryEngine:
    def __init__(self, csv_text):
        self.records = self._parse_csv(csv_text)
        self.selected_columns = None
        self.filters = []
        self.order_by_column = None
        self.order_direction = None
        self.limit_count = None

    def _parse_csv(self, csv_text):
        lines = csv_text.strip().splitlines()
        if not lines or len(lines) < 1:
            raise ValueError("CSV text must include a header row")
        
        reader = csv.reader(lines, quotechar='"', skipinitialspace=True)
        header = next(reader)
        
        if not header:
            return []
        
        records = []
        for row in reader:
            if len(row) != len(header):
                continue
            record = {header[i]: row[i] for i in range(len(header))}
            records.append(record)
        return records

    def select(self, *columns):
        self.selected_columns = columns
        return self

    def where(self, column, operator, value):
        if self.selected_columns and column not in self.selected_columns:
            raise ValueError(f"Unknown column: {column}")
        self.filters.append((column, operator, value))
        return self

    def order_by(self, column, direction):
        if self.selected_columns and column not in self.selected_columns:
            raise ValueError(f"Unknown column: {column}")
        if direction not in ["asc", "desc"]:
            raise ValueError("Invalid sort direction; use 'asc' or 'desc'")
        self.order_by_column = column
        self.order_direction = direction
        return self

    def limit(self, count):
        if count < 0:
            raise ValueError("Limit must be non-negative")
        self.limit_count = count
        return self

    def count(self):
        return len(self._apply_filters(self.records))

    def _apply_filters(self, records):
        for column, operator, value in self.filters:
            records = [record for record in records if self._compare(record[column], operator, value)]
        return records

    def _compare(self, record_value, operator, comparison_value):
        try:
            record_value = float(record_value)
            comparison_value = float(comparison_value)
            numeric_comparison = True
        except ValueError:
            numeric_comparison = False

        if operator == '=':
            return record_value == comparison_value if numeric_comparison else record_value == comparison_value
        elif operator == '!=':
            return record_value != comparison_value if numeric_comparison else record_value != comparison_value
        elif operator == '>':
            return record_value > comparison_value if numeric_comparison else record_value > comparison_value
        elif operator == '<':
            return record_value < comparison_value if numeric_comparison else record_value < comparison_value
        elif operator == '>=':
            return record_value >= comparison_value if numeric_comparison else record_value >= comparison_value
        elif operator == '<=':
            return record_value <= comparison_value if numeric_comparison else record_value <= comparison_value
        else:
            raise ValueError("Unknown operator")

    def _apply_ordering(self, records):
        if self.order_by_column:
            records = sorted(records, key=lambda r: (self._convert_value(r[self.order_by_column]) if self.order_direction == "asc" else -self._convert_value(r[self.order_by_column])), reverse=self.order_direction == "desc")
        return records

    def _convert_value(self, value):
        try:
            return float(value)
        except ValueError:
            return value

    def execute(self):
        filtered_records = self._apply_filters(self.records)
        ordered_records = self._apply_ordering(filtered_records)
        
        if self.limit_count is not None:
            ordered_records = ordered_records[:self.limit_count]
        
        if self.selected_columns:
            return [{col: record[col] for col in self.selected_columns} for record in ordered_records]
        
        return ordered_records
