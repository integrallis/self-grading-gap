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
                continue  # Handle malformed rows gracefully
            record = {header[i]: row[i] for i in range(len(header))}
            records.append(record)

        return records

    def select(self, *columns: str) -> 'CSVQueryEngine':
        if self.records:
            invalid_columns = [col for col in columns if col not in self.records[0]]
            if invalid_columns:
                raise ValueError(f"Unknown column(s): {', '.join(invalid_columns)}")
            
            self.selected_columns = columns
            self.records = [{col: record[col] for col in columns} for record in self.records]
        return self

    def where(self, column: str, operator: str, value: Any) -> 'CSVQueryEngine':
        if self.selected_columns and column not in self.selected_columns:
            raise ValueError(f"Unknown column: {column}")
        
        def compare(val1: str, val2: str, op: str) -> bool:
            if val1.isdigit() and val2.isdigit():
                val1, val2 = int(val1), int(val2)
            if op == '=':
                return val1 == val2
            elif op == '!=':
                return val1 != val2
            elif op == '>':
                return val1 > val2
            elif op == '<':
                return val1 < val2
            elif op == '>=':
                return val1 >= val2
            elif op == '<=':
                return val1 <= val2
            else:
                raise ValueError("Unknown operator")

        self.records = [record for record in self.records if compare(record[column], value, operator)]
        return self

    def order_by(self, column: str, direction: str = "asc") -> 'CSVQueryEngine':
        if self.selected_columns and column not in self.selected_columns:
            raise ValueError(f"Unknown column: {column}")

        if direction not in ["asc", "desc"]:
            raise ValueError("Invalid sort direction; use 'asc' or 'desc'")

        self.records.sort(key=lambda record: (float(record[column]) if record[column].isdigit() else record[column]), reverse=(direction == "desc"))
        return self

    def limit(self, n: int) -> List[Dict[str, str]]:
        if n < 0:
            raise ValueError("Limit must be non-negative")
        if n == 0:
            return []
        return self.records[:n]

    def count(self) -> int:
        return len(self.records)

# Example usage:
# csv_text = """name,age,height\nAlice,30,5.5\nBob,25,6.0"""
# engine = CSVQueryEngine(csv_text)
# result = engine.select("name").where("age", ">", "28").order_by("name").limit(10)
# print(result)
