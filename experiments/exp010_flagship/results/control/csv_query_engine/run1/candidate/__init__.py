def read_csv(csv_text):
    lines = csv_text.strip().split('\n')
    if not lines or len(lines) < 1:
        return []
    header = lines[0].split(',')
    if len(header) < 1:
        raise ValueError("CSV text must include a header row")
    records = []
    for line in lines[1:]:
        values = line.split(',')
        record = {header[i]: values[i] if i < len(values) else '' for i in range(len(header))}
        records.append(record)
    return records


def project(records, columns):
    return [{col: record[col] for col in columns if col in record} for record in records]


def filter(records, column, operator, value):
    if not records or column not in records[0]:
        raise ValueError("unknown column")
    if operator not in {'=', '!=', '>', '<'}:
        raise ValueError("unknown operator")
    if operator == '=':
        return [record for record in records if record[column] == value]
    elif operator == '!=':
        return [record for record in records if record[column] != value]
    elif operator == '>':
        return [record for record in records if float(record[column]) > float(value)]
    elif operator == '<':
        return [record for record in records if float(record[column]) < float(value)]


def order(records, column, direction):
    if direction not in {'asc', 'desc'}:
        raise ValueError("accepted 'asc' direction")
    return sorted(records, key=lambda x: float(x[column]), reverse=(direction == 'desc'))


def limit(records, n):
    if n < 0:
        raise ValueError("non-negative")
    return records[:n]


def count(records):
    return len(records)