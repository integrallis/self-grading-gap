# your complete test file
import pytest
from solution import csv_query_engine

def test_read_csv_with_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    expected_records = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert records == expected_records

def test_read_csv_with_no_records():
    csv_text = "name,age"
    records = csv_query_engine.read_csv(csv_text)
    expected_records = []
    assert records == expected_records
    assert csv_query_engine.count(records) == 0

def test_read_csv_with_quoted_field():
    csv_text = "name,age\n\"Alice, the one who loves coding\",30"
    records = csv_query_engine.read_csv(csv_text)
    expected_records = [
        {"name": "Alice, the one who loves coding", "age": "30"}
    ]
    assert records == expected_records

def test_read_csv_with_spaces_in_headers():
    csv_text = "first name,age\nAlice,30"
    records = csv_query_engine.read_csv(csv_text)
    expected_records = [
        {"first name": "Alice", "age": "30"}
    ]
    assert records == expected_records

def test_read_csv_without_header():
    csv_text = "Alice,30\nBob,25"
    with pytest.raises(ValueError, match="CSV text must include a header row"):
        csv_query_engine.read_csv(csv_text)

def test_project_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    projected = csv_query_engine.project(records, ["name"])
    expected = [
        {"name": "Alice"},
        {"name": "Bob"}
    ]
    assert projected == expected

def test_project_columns_order():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    projected = csv_query_engine.project(records, ["age", "name"])
    expected = [
        {"age": "30", "name": "Alice"},
        {"age": "25", "name": "Bob"}
    ]
    assert projected == expected

def test_filter_rows_equality():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", "=", "30")
    expected = [
        {"name": "Alice", "age": "30"}
    ]
    assert filtered == expected

def test_filter_rows_numeric_comparison():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", ">", "25")
    expected = [
        {"name": "Alice", "age": "30"}
    ]
    assert filtered == expected

def test_filter_rows_invalid_operator():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    with pytest.raises(ValueError, match="unknown operator"):
        csv_query_engine.filter(records, "age", "invalid", "30")

def test_order_rows_ascending():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    ordered = csv_query_engine.order(records, "age", "asc")
    expected = [
        {"name": "Bob", "age": "25"},
        {"name": "Alice", "age": "30"}
    ]
    assert ordered == expected

def test_order_rows_descending():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    ordered = csv_query_engine.order(records, "age", "desc")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert ordered == expected

def test_limit_records():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)
    limited = csv_query_engine.limit(records, 2)
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert limited == expected

def test_limit_records_greater_than_count():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    limited = csv_query_engine.limit(records, 5)
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert limited == expected

def test_limit_zero_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    limited = csv_query_engine.limit(records, 0)
    expected = []
    assert limited == expected

def test_limit_negative():
    csv_text = "name,age\nAlice,30"
    records = csv_query_engine.read_csv(csv_text)
    with pytest.raises(ValueError, match="non-negative"):
        csv_query_engine.limit(records, -1)

def test_count_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    count = csv_query_engine.count(records)
    assert count == 2

def test_count_filtered_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    filtered = csv_query_engine.filter(records, "age", ">", "25")
    count = csv_query_engine.count(filtered)
    assert count == 1

def test_composed_queries():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)
    result = csv_query_engine.filter(records, "age", ">", "25")
    result = csv_query_engine.order(result, "age", "asc")
    result = csv_query_engine.limit(result, 1)
    expected = [
        {"name": "Charlie", "age": "35"}
    ]
    assert result == expected

def test_filter_invalid_column():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    with pytest.raises(ValueError, match="unknown column"):
        csv_query_engine.filter(records, "invalid_column", "=", "30")