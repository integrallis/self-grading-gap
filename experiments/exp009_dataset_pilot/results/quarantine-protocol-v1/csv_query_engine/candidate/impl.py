import csv
from typing import List, Dict, Any, Union

class CSVQueryEngine:
    def __init__(self, csv_text: str):
        self.records = self.parse_csv(csv_text)
        self.columns = list(self.records[0].keys()) if self.records else []
        self.filtered_records = self.records

    def parse_csv(self, csv_text: str) -> List[Dict[str, str]]:
        lines = csv_text.strip().splitlines()
        if not lines:
            raise ValueError("CSV text must include a header row")
        reader = csv.reader(lines)
        headers = next(reader)
        if not headers:
            return []
        self.validate_headers(headers)
        return [{header: value for header, value in zip(headers, row)} for row in reader]

    def validate_headers(self, headers: List[str]):
        for header in headers:
            if not header.strip():
                raise ValueError("Header names cannot be empty")

    def select(self, *columns: str) -> 'CSVQueryEngine':
        self.validate_columns(columns)
        self.filtered_records = [{col: record[col] for col in columns} for record in self.filtered_records]
        self.columns = list(columns)
        return self

    def validate_columns(self, columns: List[str]):
        unknown_columns = [col for col in columns if col not in self.columns]
        if unknown_columns:
            raise ValueError(f"Unknown column(s): {', '.join(unknown_columns)}")

    def where(self, column: str, operator: str, value: str) -> 'CSVQueryEngine':
        self.validate_columns([column])
        self.filtered_records = [record for record in self.filtered_records if self.compare(record[column], operator, value)]
        return self

    def compare(self, record_value: str, operator: str, comparison_value: str) -> bool:
        try:
            record_value_num = float(record_value)
            comparison_value_num = float(comparison_value)
            numeric_comparison = True
        except ValueError:
            numeric_comparison = False

        if operator == '=':
            return (numeric_comparison and record_value_num == comparison_value_num) or (not numeric_comparison and record_value == comparison_value)
        elif operator == '!=':
            return (numeric_comparison and record_value_num != comparison_value_num) or (not numeric_comparison and record_value != comparison_value)
        elif operator == '>':
            return record_value_num > comparison_value_num if numeric_comparison else record_value > comparison_value
        elif operator == '<':
            return record_value_num < comparison_value_num if numeric_comparison else record_value < comparison_value
        elif operator == '>=':
            return record_value_num >= comparison_value_num if numeric_comparison else record_value >= comparison_value
        elif operator == '<=':
            return record_value_num <= comparison_value_num if numeric_comparison else record_value <= comparison_value
        else:
            raise ValueError("unknown operator")

    def order_by(self, column: str, direction: str = 'asc') -> 'CSVQueryEngine':
        self.validate_columns([column])
        if direction not in ['asc', 'desc']:
            raise ValueError("Invalid sort direction; accepted values are 'asc' and 'desc'")

        self.filtered_records.sort(key=lambda x: (float(x[column]) if self.is_numeric(x[column]) else x[column]), 
                                    reverse=(direction == 'desc'))
        return self

    def is_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def limit(self, n: int) -> 'CSVQueryEngine':
        if n < 0:
            raise ValueError("Limit must be non-negative")
        self.filtered_records = self.filtered_records[:n]
        return self

    def count(self) -> int:
        return len(self.filtered_records)

    def materialize(self) -> List[Dict[str, str]]:
        return self.filtered_records

# Example usage (uncomment to test):
# csv_text = """name,age,city
# "Alice, A",30,"New York"
# "Bob",25,"Los Angeles"
# "Charlie",35,"Chicago" """
# engine = CSVQueryEngine(csv_text)
# results = engine.select('name', 'age').where('age', '>', '28').order_by('age', 'asc').limit(2).materialize()
# print(results)
