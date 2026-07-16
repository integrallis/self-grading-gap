def read_csv(csv_text):
    import csv
    from io import StringIO
    csv_reader = csv.DictReader(StringIO(csv_text))
    records = [row for row in csv_reader]
    if len(csv_text.strip()) > 0 and not records:
        raise ValueError("CSV text must include a header row")
    return records


def project(records, columns):
    if not records:
        return []
    for col in columns:
        if col not in records[0]:
            raise ValueError(f"unknown column: {col}")
    return [{col: record[col] for col in columns} for record in records]


def filter(records, column, operator, value):
    if not records:
        return []
    if column not in records[0]:
        raise ValueError(f"unknown column: {column}")
    if operator not in ('=', '!=', '<', '<=', '>', '>='):
        raise ValueError(f"unknown operator: {operator}")
    filtered = []
    for record in records:
        record_value = record[column]
        if operator == '=' and record_value == value:
            filtered.append(record)
        elif operator == '!=' and record_value != value:
            filtered.append(record)
        elif operator == '<' and float(record_value) < float(value):
            filtered.append(record)
        elif operator == '<=' and float(record_value) <= float(value):
            filtered.append(record)
        elif operator == '>' and float(record_value) > float(value):
            filtered.append(record)
        elif operator == '>=' and float(record_value) >= float(value):
            filtered.append(record)
    return filtered


def order(records, column, direction):
    if not records:
        return []
    if column not in records[0]:
        raise ValueError(f"unknown column: {column}")
    if direction not in ('asc', 'desc'):
        raise ValueError(f"unknown direction: {direction}. Expected 'asc' or 'desc'.")
    return sorted(records, key=lambda x: float(x[column]) if x[column].isdigit() else x[column], reverse=(direction == 'desc'))


def limit(records, count):
    if count < 0:
        raise ValueError("count must be non-negative")
    return records[:count]


def count(records):
    return len(records)