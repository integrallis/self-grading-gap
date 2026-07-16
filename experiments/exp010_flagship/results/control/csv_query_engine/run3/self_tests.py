# test_csv_query_engine.py

import pytest
from solution import read_csv, project, filter, order, limit, count

# US-1: Read CSV text into records
def test_read_csv_with_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert read_csv(csv_text) == expected

def test_read_csv_empty():
    csv_text = "name,age"
    expected = []
    assert read_csv(csv_text) == expected
    assert count(read_csv(csv_text)) == 0

def test_read_csv_with_quoted_field():
    csv_text = 'name,description\n"Bob, the Builder",35'
    expected = [{'name': 'Bob, the Builder', 'description': '35'}]
    assert read_csv(csv_text) == expected

def test_read_csv_with_spaces_in_header():
    csv_text = "first name,age\nAlice,30\nBob,25"
    expected = [{'first name': 'Alice', 'age': '30'}, {'first name': 'Bob', 'age': '25'}]
    assert read_csv(csv_text) == expected

def test_read_csv_without_header():
    csv_text = "Alice,30\nBob,25"
    with pytest.raises(ValueError) as excinfo:
        read_csv(csv_text)
    assert str(excinfo.value) == "CSV text must include a header row"

# US-2: Choose columns
def test_project_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert project(records, ['name']) == expected

def test_project_columns_order():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'age': '30', 'name': 'Alice'}, {'age': '25', 'name': 'Bob'}]
    assert project(records, ['age', 'name']) == expected

def test_project_with_filtering():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    filtered_records = filter(records, 'age', '>=', '30')
    projected = project(filtered_records, ['name'])
    expected = [{'name': 'Alice'}]
    assert projected == expected

# US-3: Filter rows
def test_filter_equality():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Alice', 'age': '30'}]
    assert filter(records, 'name', '=', 'Alice') == expected

def test_filter_inequality():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Bob', 'age': '25'}]
    assert filter(records, 'name', '!=', 'Alice') == expected

def test_filter_numeric_comparison():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Bob', 'age': '25'}]
    assert filter(records, 'age', '<', '30') == expected

def test_filter_invalid_operator():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    with pytest.raises(ValueError) as excinfo:
        filter(records, 'age', 'invalid_op', '30')
    assert "unknown operator" in str(excinfo.value)

def test_filter_mixed_types():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Bob', 'age': '25'}]
    assert filter(records, 'age', '>', '20') == expected

# US-4: Order rows
def test_order_ascending_numeric():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}]
    assert order(records, 'age', 'asc') == expected

def test_order_descending_numeric():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert order(records, 'age', 'desc') == expected

def test_order_alphabetical():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert order(records, 'name', 'asc') == expected

def test_order_invalid_direction():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    with pytest.raises(ValueError) as excinfo:
        order(records, 'age', 'invalid_dir')
    assert "asc" in str(excinfo.value)

# US-5: Limit and count
def test_limit_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Alice', 'age': '30'}]
    assert limit(records, 1) == expected

def test_limit_greater_than_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert limit(records, 3) == expected

def test_limit_zero():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    expected = []
    assert limit(records, 0) == expected

def test_limit_negative():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    with pytest.raises(ValueError) as excinfo:
        limit(records, -1)
    assert "non-negative" in str(excinfo.value)

def test_count_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    assert count(records) == 2

def test_count_filtered_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    filtered_records = filter(records, 'age', '>=', '30')
    assert count(filtered_records) == 1

# US-6: Compose queries predictably
def test_chained_operations():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    filtered = filter(records, 'age', '>=', '25')
    ordered = order(filtered, 'name', 'asc')
    limited = limit(ordered, 1)
    expected = [{'name': 'Alice', 'age': '30'}]
    assert limited == expected

def test_projecting_invalid_column():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    with pytest.raises(ValueError) as excinfo:
        project(records, ['non_existing_column'])
    assert "unknown column" in str(excinfo.value)

def test_filtering_invalid_column():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    with pytest.raises(ValueError) as excinfo:
        filter(records, 'non_existing_column', '=', 'Alice')
    assert "unknown column" in str(excinfo.value)

def test_single_record_operations():
    csv_text = "name,age\nAlice,30"
    records = read_csv(csv_text)
    filtered = filter(records, 'age', '>=', '30')
    ordered = order(filtered, 'name', 'asc')
    limited = limit(ordered, 1)
    assert count(limited) == 1