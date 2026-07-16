import csv
from typing import List, Dict, Any


class CSVQueryEngine:
    def __init__(self, csv_text: str):
        self.records = self._parse_csv(csv_text)
        self.selected_columns = None

    def _parse_csv(self, csv_text: str) -> List[Dict[str, str]]:
        lines = csv_text.strip().splitlines()
        if not lines:
            raise ValueError("CSV text must include a header row")
        
        reader = csv.reader(lines)
        header = next(reader)
        if not header:
            return []

        self.header = [h.strip() for h in header]
        records = []
        for row in reader:
            if row:
                record = {}
                for i in range(len(self.header)):
                    if i < len(row):
                        record[self.header[i]] = str(row[i])
                records.append(record)
        return records

    def select(self, *columns: str) -> 'CSVQueryEngine':
        self.selected_columns = []
        for col in columns:
            if col in self.header:
                self.selected_columns.append(col)
        return self

    def where(self, column: str, operator: str, value: str) -> 'CSVQueryEngine':
        if column not in self.header:
            raise ValueError(f"Unknown column: {column}")
        
        if operator not in ('=', '!=', '>', '<', '>=', '<='):
            raise ValueError("Unknown operator")
        
        numeric_value = self._try_parse_number(value)
        filtered_records = []
        for record in self.records:
            if self._compare(record.get(column), operator, numeric_value):
                filtered_records.append(record)
        self.records = filtered_records
        return self

    def order_by(self, column: str, direction: str = 'asc') -> 'CSVQueryEngine':
        if column not in (self.selected_columns if self.selected_columns else self.header):
            raise ValueError(f"Unknown column: {column}")
        if direction not in ('asc', 'desc'):
            raise ValueError("Invalid sort direction; accepted: 'asc', 'desc'")

        self.records.sort(key=lambda record: self._get_sort_key(record[column]), reverse=(direction == 'desc'))
        return self

    def limit(self, n: int) -> 'CSVQueryEngine':
        if n < 0:
            raise ValueError("Limit must be non-negative")
        self.records = self.records[:n]
        return self

    def count(self) -> int:
        return len(self.records)

    def materialize(self) -> List[Dict[str, Any]]:
        if self.selected_columns:
            materialized_records = []
            for record in self.records:
                materialized_record = {}
                for col in self.selected_columns:
                    materialized_record[col] = record[col]
                materialized_records.append(materialized_record)
            return materialized_records
        return self.records

    def _compare(self, record_value: str, operator: str, comparison_value: Any) -> bool:
        if operator == '=':
            return record_value == str(comparison_value)
        elif operator == '!=':
            return record_value != str(comparison_value)
        elif operator == '>':
            return self._compare_numeric(record_value, comparison_value) > 0
        elif operator == '<':
            return self._compare_numeric(record_value, comparison_value) < 0
        elif operator == '>=':
            return self._compare_numeric(record_value, comparison_value) >= 0
        elif operator == '<=':
            return self._compare_numeric(record_value, comparison_value) <= 0
        return False

    def _compare_numeric(self, record_value: str, comparison_value: Any) -> int:
        try:
            record_numeric = float(record_value)
            return (record_numeric > comparison_value) - (record_numeric < comparison_value)
        except ValueError:
            return (record_value > str(comparison_value)) - (record_value < str(comparison_value))

    def _try_parse_number(self, value: str) -> Any:
        try:
            return float(value)
        except ValueError:
            return value

    def _get_sort_key(self, value: str) -> Any:
        try:
            return float(value)
        except ValueError:
            return value
