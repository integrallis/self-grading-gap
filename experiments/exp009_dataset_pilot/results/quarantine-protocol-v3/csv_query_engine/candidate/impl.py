import csv
from typing import List, Dict, Any, Union

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

        records = []
        for row in reader:
            if len(row) != len(header):
                continue
            record = {header[i]: row[i] for i in range(len(header))}
            records.append(record)
        return records

    def select(self, *columns: str) -> 'CSVQueryEngine':
        self.selected_columns = columns
        return self

    def where(self, column: str, operator: str, value: str) -> 'CSVQueryEngine':
        if self.selected_columns is not None and column not in self.selected_columns:
            raise ValueError(f"Unknown column: {column}")
        if operator not in ['=', '!=', '>', '<', '>=', '<=']:
            raise ValueError("unknown operator")
        
        filtered_records = []
        for record in self.records:
            if column not in record:
                raise ValueError(f"Unknown column: {column}")
            
            record_value = record[column]
            comparison_value = self._convert_value(value)
            if operator == '=' and record_value == comparison_value:
                filtered_records.append(record)
            elif operator == '!=' and record_value != comparison_value:
                filtered_records.append(record)
            elif operator == '>' and self._compare(record_value, comparison_value) > 0:
                filtered_records.append(record)
            elif operator == '<' and self._compare(record_value, comparison_value) < 0:
                filtered_records.append(record)
            elif operator == '>=' and self._compare(record_value, comparison_value) >= 0:
                filtered_records.append(record)
            elif operator == '<=' and self._compare(record_value, comparison_value) <= 0:
                filtered_records.append(record)
        
        self.records = filtered_records
        return self

    def order_by(self, column: str, direction: str = 'asc') -> 'CSVQueryEngine':
        if self.selected_columns is not None and column not in self.selected_columns:
            raise ValueError(f"Unknown column: {column}")
        if direction not in ['asc', 'desc']:
            raise ValueError("Invalid sort direction; use 'asc' or 'desc'")

        self.records.sort(key=lambda r: self._convert_value(r[column]), reverse=(direction == 'desc'))
        return self

    def limit(self, n: int) -> 'CSVQueryEngine':
        if n < 0:
            raise ValueError("Limit must be non-negative")
        self.records = self.records[:n]
        return self

    def count(self) -> int:
        return len(self.records)

    def materialize(self) -> List[Dict[str, str]]:
        if self.selected_columns is None:
            return self.records
        return [{col: record[col] for col in self.selected_columns if col in record} for record in self.records]

    def _convert_value(self, value: str) -> Union[str, int, float]:
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value

    def _compare(self, value1: str, value2: str) -> int:
        num1, num2 = self._convert_value(value1), self._convert_value(value2)
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            return (num1 > num2) - (num1 < num2)
        return (value1 > value2) - (value1 < value2)
