import pytest
from solution import CSVQueryEngine

def test_read_csv_with_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert engine.records == expected

def test_read_csv_with_no_records():
    csv_text = "name,age"
    engine = CSVQueryEngine(csv_text)
    expected = []
    assert engine.records == expected
    assert engine.count() == 0
    assert engine.project(["name"]).records == []
    assert engine.filter_by('age', '>', '20').records == []

def test_read_csv_with_quoted_fields():
    csv_text = "name,age\n\"Doe, John\",40"
    engine = CSVQueryEngine(csv_text)
    expected = [{'name': 'Doe, John', 'age': '40'}]
    assert engine.records == expected

def test_read_csv_with_header_names_containing_spaces():
    csv_text = "first name,age\nAlice,30"
    engine = CSVQueryEngine(csv_text)
    expected = [{'first name': 'Alice', 'age': '30'}]
    assert engine.records == expected

def test_read_csv_without_header_row():
    csv_text = ""
    with pytest.raises(Exception) as excinfo:
        CSVQueryEngine(csv_text)
    assert str(excinfo.value) == "CSV text must include a header row"

def test_project_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    projected = engine.project(["name"])
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert projected.records == expected

def test_project_columns_order():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    projected = engine.project(["age", "name"])
    expected = [{'age': '30', 'name': 'Alice'}, {'age': '25', 'name': 'Bob'}]
    assert projected.records == expected
    assert list(projected.records[0]) == ["age", "name"]

def test_filter_equals():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    filtered = engine.filter_by('age', '=', '30')
    expected = [{'name': 'Alice', 'age': '30'}]
    assert filtered.records == expected

def test_filter_not_equals():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    filtered = engine.filter_by('age', '!=', '30')
    expected = [{'name': 'Bob', 'age': '25'}]
    assert filtered.records == expected

def test_filter_multiple_matches():
    csv_text = "name,age\nAlice,30\nBob,30\nCharlie,25"
    engine = CSVQueryEngine(csv_text)
    filtered = engine.filter_by('age', '=', '30')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '30'}]
    assert filtered.records == expected  # Check input order preserved

def test_order_by_ascending():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,10"
    engine = CSVQueryEngine(csv_text)
    ordered = engine.order_by('age', 'asc')
    expected = [{'name': 'Charlie', 'age': '10'}, {'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}]
    assert ordered.records == expected

def test_order_by_descending():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    ordered = engine.order_by('age', 'desc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert ordered.records == expected

def test_order_by_numerical_stability():
    csv_text = "name,age\nAlice,30\nBob,30\nCharlie,25"
    engine = CSVQueryEngine(csv_text)
    ordered = engine.order_by('age', 'asc')
    expected = [{'name': 'Charlie', 'age': '25'}, {'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '30'}]
    assert ordered.records == expected  # Check stability

def test_order_by_textual():
    csv_text = "name,age\nCharlie,30\nAlice,25\nBob,25"
    engine = CSVQueryEngine(csv_text)
    ordered = engine.order_by('name', 'asc')
    expected = [{'name': 'Alice', 'age': '25'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '30'}]
    assert ordered.records == expected

def test_limit():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    engine = CSVQueryEngine(csv_text)
    limited = engine.limit(2)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert limited.records == expected

def test_limit_greater_than_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    limited = engine.limit(5)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert limited.records == expected

def test_limit_zero():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    limited = engine.limit(0)
    expected = []
    assert limited.records == expected

def test_limit_negative():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    with pytest.raises(Exception) as excinfo:
        engine.limit(-1)
    assert "non-negative" in str(excinfo.value)

def test_count_all_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    total = engine.count()
    expected = 2
    assert total == expected

def test_count_filtered_records():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    filtered = engine.filter_by('age', '>', '26')
    total = filtered.count()
    expected = 1
    assert total == expected

def test_count_zero_records():
    csv_text = "name,age"
    engine = CSVQueryEngine(csv_text)
    total = engine.count()
    expected = 0
    assert total == expected

def test_chained_operations():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    engine = CSVQueryEngine(csv_text)
    result = engine.filter_by('age', '>', '26').order_by('age', 'asc').limit(1)
    expected = [{'name': 'Alice', 'age': '30'}]  # Filters to Alice, orders, limits to 1
    assert result.records == expected

def test_unknown_operator():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    with pytest.raises(Exception) as excinfo:
        engine.filter_by('age', '~=', '30')
    assert "unknown operator" in str(excinfo.value)

def test_unknown_column_filter():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    with pytest.raises(Exception) as excinfo:
        engine.filter_by('height', '=', '5.5')
    assert "unknown column 'height'" in str(excinfo.value)

def test_unknown_column_project():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    with pytest.raises(Exception) as excinfo:
        engine.project(['height'])
    assert "unknown column 'height'" in str(excinfo.value)

def test_unknown_column_order():
    csv_text = "name,age\nAlice,30\nBob,25"
    engine = CSVQueryEngine(csv_text)
    with pytest.raises(Exception) as excinfo:
        engine.order_by('height', 'asc')
    assert "unknown column 'height'" in str(excinfo.value)

def test_limit_then_filter():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    engine = CSVQueryEngine(csv_text)
    result = engine.limit(2).filter_by('age', '>', '26')
    expected = [{'name': 'Alice', 'age': '30'}]
    assert result.records == expected

def test_filter_then_limit():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    engine = CSVQueryEngine(csv_text)
    result = engine.filter_by('age', '>', '26').limit(1)
    expected = [{'name': 'Alice', 'age': '30'}]
    assert result.records == expected

def test_single_record_full_chain():
    csv_text = "name,age\nAlice,30"
    engine = CSVQueryEngine(csv_text)
    result = engine.filter_by('age', '>', '26').order_by('age', 'asc').limit(1).count()
    expected = 1
    assert result == expected