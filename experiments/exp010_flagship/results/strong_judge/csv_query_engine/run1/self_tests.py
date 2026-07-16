import pytest
from solution import csv_query_engine  # Assuming the main function to test is in csv_query_engine.py

def test_read_csv_with_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]
    assert csv_query_engine.parse_csv(csv_text) == expected

def test_read_csv_with_no_records():
    csv_text = "name,age"
    expected = []
    assert csv_query_engine.parse_csv(csv_text) == expected

def test_read_csv_with_quoted_field():
    csv_text = 'name,description\n"Smith, John","A developer"'
    expected = [
        {"name": "Smith, John", "description": "A developer"},
    ]
    assert csv_query_engine.parse_csv(csv_text) == expected

def test_read_csv_with_spaces_in_header():
    csv_text = "first name,last name\nJohn,Doe"
    expected = [
        {"first name": "John", "last name": "Doe"},
    ]
    assert csv_query_engine.parse_csv(csv_text) == expected

def test_read_csv_without_header():
    csv_text = ""
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.parse_csv(csv_text)
    assert str(excinfo.value) == "CSV text must include a header row"

def test_project_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    projected = csv_query_engine.project(records, ["name"])
    expected = [
        {"name": "Alice"},
        {"name": "Bob"},
    ]
    assert projected == expected

def test_project_columns_order():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    projected = csv_query_engine.project(records, ["age", "name"])
    expected = [
        {"age": "30", "name": "Alice"},
        {"age": "25", "name": "Bob"},
    ]
    assert projected == expected

def test_project_columns_with_spaces():
    csv_text = "first name,last name\nJohn,Doe"
    records = csv_query_engine.parse_csv(csv_text)
    projected = csv_query_engine.project(records, ["first name"])
    expected = [
        {"first name": "John"},
    ]
    assert projected == expected

def test_filter_equal():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", "=", "30")
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert filtered == expected

def test_filter_inequality():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", "!=", "30")
    expected = [
        {"name": "Bob", "age": "25"},
    ]
    assert filtered == expected

def test_order_ascending_numeric():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,9"
    records = csv_query_engine.parse_csv(csv_text)
    ordered = csv_query_engine.order(records, "age", "asc")
    expected = [
        {"name": "Charlie", "age": "9"},
        {"name": "Bob", "age": "25"},
        {"name": "Alice", "age": "30"},
    ]
    assert ordered == expected

def test_order_ascending_ties():
    csv_text = "name,age\nAlice,30\nBob,30"
    records = csv_query_engine.parse_csv(csv_text)
    ordered = csv_query_engine.order(records, "age", "asc")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "30"},
    ]
    assert ordered == expected

def test_order_descending():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,9"
    records = csv_query_engine.parse_csv(csv_text)
    ordered = csv_query_engine.order(records, "age", "desc")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
        {"name": "Charlie", "age": "9"},
    ]
    assert ordered == expected

def test_limit():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    limited = csv_query_engine.limit(records, 1)
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert limited == expected

def test_count():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    count = csv_query_engine.count(records)
    expected = 2  # There are two records
    assert count == expected

def test_count_empty():
    csv_text = "name,age"
    records = csv_query_engine.parse_csv(csv_text)
    count = csv_query_engine.count(records)
    expected = 0  # No records
    assert count == expected

def test_limit_zero():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    limited = csv_query_engine.limit(records, 0)
    expected = []
    assert limited == expected

def test_limit_negative():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.limit(records, -1)
    assert "non-negative" in str(excinfo.value)

def test_limit_larger_than_count():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    limited = csv_query_engine.limit(records, 5)
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]
    assert limited == expected

def test_filter_unknown_operator():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.filter(records, "age", "unknown", "30")
    assert "unknown operator" in str(excinfo.value)

def test_order_unknown_direction():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.order(records, "age", "unknown")
    assert "asc" in str(excinfo.value)

def test_chain_operations():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", ">", "25")
    ordered = csv_query_engine.order(filtered, "age", "asc")
    limited = csv_query_engine.limit(ordered, 1)
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert limited == expected

def test_single_record_chain_operations():
    csv_text = "name,age\nAlice,30"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", "=", "30")
    ordered = csv_query_engine.order(filtered, "name", "asc")
    limited = csv_query_engine.limit(ordered, 1)
    count = csv_query_engine.count(limited)
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert limited == expected
    assert count == 1

def test_chain_operations_different_order():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.parse_csv(csv_text)
    limited = csv_query_engine.limit(records, 2)
    filtered = csv_query_engine.filter(limited, "age", ">", "25")
    ordered = csv_query_engine.order(filtered, "age", "asc")
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert ordered == expected

def test_unknown_column_projection():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.project(records, ["unknown"])
    assert "unknown" in str(excinfo.value)

def test_unknown_column_filter():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.filter(records, "unknown", "=", "30")
    assert "unknown" in str(excinfo.value)

def test_unknown_column_order():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    with pytest.raises(Exception) as excinfo:
        csv_query_engine.order(records, "unknown", "asc")
    assert "unknown" in str(excinfo.value)

def test_filter_numeric_boundary():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,10"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", ">", "25")
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert filtered == expected

    filtered = csv_query_engine.filter(records, "age", "<=", "30")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
        {"name": "Charlie", "age": "10"},
    ]
    assert filtered == expected

def test_filter_numeric_equality():
    csv_text = "name,age\nAlice,30\nBob,30.0"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", "=", "30.0")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "30.0"},
    ]
    assert filtered == expected

def test_filter_textual_fallback():
    csv_text = "name,age\nAlice,30\nBob,10x"
    records = csv_query_engine.parse_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", ">", "10")
    expected = [
        {"name": "Alice", "age": "30"},
    ]
    assert filtered == expected

def test_order_textual():
    csv_text = "name,age\nCharlie,30\nAlice,25\nBob,25"
    records = csv_query_engine.parse_csv(csv_text)
    ordered = csv_query_engine.order(records, "name", "asc")
    expected = [
        {"name": "Alice", "age": "25"},
        {"name": "Bob", "age": "25"},
        {"name": "Charlie", "age": "30"},
    ]
    assert ordered == expected