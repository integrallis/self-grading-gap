def read_csv(csv_text):
    lines = csv_text.strip().split('\n')
    if len(lines) < 2:
        raise ValueError('CSV text must include a header row')
    headers = [h.strip() for h in lines[0].split(',')]
    records = []
    for line in lines[1:]:
        values = [v.strip().strip('"') for v in line.split(',')]
        records.append(dict(zip(headers, values)))
    return records


def count(records):
    return len(records)


def project(records, columns):
    return [{col: record[col] for col in columns} for record in records]


def filter(records, column, operator, value):
    if column not in records[0]:
        raise ValueError('unknown column')
    if operator not in {'=', '>', '<'}:
        raise ValueError('unknown operator')
    if operator == '=':
        return [r for r in records if r[column] == value]
    elif operator == '>':
        return [r for r in records if float(r[column]) > float(value)]
    elif operator == '<':
        return [r for r in records if float(r[column]) < float(value)]


def order(records, column, direction):
    if direction not in {'asc', 'desc'}:
        raise ValueError('unknown direction')
    return sorted(records, key=lambda r: float(r[column]), reverse=(direction == 'desc'))


def limit(records, n):
    if n < 0:
        raise ValueError('non-negative')
    return records[:n]