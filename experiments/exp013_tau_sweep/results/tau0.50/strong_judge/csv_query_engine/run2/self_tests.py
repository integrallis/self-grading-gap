import pytest
from solution import csv_query_engine

def test_read_csv_into_records_no_header():
    # Input is genuinely headerless CSV
    with pytest.raises(Exception) as exc:
        csv_query_engine.read_csv("")
    assert str(exc.value) == "CSV text must include a header row"  # AC-1.5

def test_read_csv_into_records_empty():
    result = csv_query_engine.read_csv("header1,header2\n")
    assert result == []  # AC-1.2: No records

def test_read_csv_into_records_with_data():
    result = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]  # AC-1.1
    assert result == expected

def test_read_csv_with_quoted_comma():
    result = csv_query_engine.read_csv('name,age\n"Smith, John",30')
    expected = [{'name': 'Smith, John', 'age': '30'}]  # AC-1.3
    assert result == expected

def test_read_csv_with_spaces_in_header():
    result = csv_query_engine.read_csv("first name,age\nAlice,30")
    expected = [{'first name': 'Alice', 'age': '30'}]  # AC-1.4
    assert result == expected

def test_projection_keeps_only_requested_columns():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.project(data, ['name'])
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]  # AC-2.1
    assert result == expected

def test_projection_order_of_columns():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.project(data, ['age', 'name'])
    expected = [{'age': '30', 'name': 'Alice'}, {'age': '25', 'name': 'Bob'}]  # AC-2.2
    assert [list(row.keys()) for row in result] == [["age", "name"], ["age", "name"]]  # Check order

def test_projection_on_header_only():
    data = csv_query_engine.read_csv("header1,header2\n")
    result = csv_query_engine.project(data, ['header1'])
    assert result == []  # AC-2.2: Projecting on empty results in empty

def test_filtering_by_equality():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '=', '30')
    expected = [{'name': 'Alice', 'age': '30'}]  # AC-3.1
    assert result == expected

def test_filtering_by_inequality():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '!=', '30')
    expected = [{'name': 'Bob', 'age': '25'}]  # AC-3.1
    assert result == expected

def test_filtering_with_numeric_comparison():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '>', '26')
    expected = [{'name': 'Alice', 'age': '30'}]  # AC-3.2
    assert result == expected

def test_filtering_with_numeric_vs_text_comparison():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '>', '35')
    expected = []  # No records match
    assert result == expected

def test_filtering_with_boundary_semantics():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '>=', '30')
    expected = [{'name': 'Alice', 'age': '30'}]  # AC-3.3
    assert result == expected

def test_filtering_with_less_than_boundary():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '<', '30')
    expected = [{'name': 'Bob', 'age': '25'}]  # AC-3.3
    assert result == expected

def test_filtering_with_greater_than_boundary():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'age', '>', '30')
    expected = []  # AC-3.3: No records match
    assert result == expected

def test_filtering_numeric_equality():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,30.0")
    result = csv_query_engine.filter(data, 'age', '=', '30.0')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '30.0'}]  # AC-3.4
    assert result == expected

def test_invalid_operator_rejected():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(Exception, match="unknown operator"):
        csv_query_engine.filter(data, 'age', '***', '30')

def test_mixed_numeric_text_comparison():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,two")
    result = csv_query_engine.filter(data, 'age', '=', 'two')
    expected = [{'name': 'Bob', 'age': 'two'}]  # AC-3.6
    assert result == expected

def test_ordering_by_numeric_column_ascending():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25\nCharlie,9")
    result = csv_query_engine.order(data, 'age', 'asc')
    expected = [{'name': 'Charlie', 'age': '9'}, {'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}]  # AC-4.1
    assert result == expected

def test_ordering_by_numeric_column_descending():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25\nCharlie,9")
    result = csv_query_engine.order(data, 'age', 'desc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '9'}]  # AC-4.2
    assert result == expected

def test_ordering_by_numeric_ties():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,30")
    result = csv_query_engine.order(data, 'age', 'asc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '30'}]  # Ties should preserve input order
    assert result == expected

def test_ordering_by_text_column():
    data = csv_query_engine.read_csv("name,age\nBob,25\nAlice,30")
    result = csv_query_engine.order(data, 'name', 'asc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]  # AC-4.3
    assert result == expected

def test_ordering_text_with_ties():
    data = csv_query_engine.read_csv("name,age\nBob,25\nAlice,30\nAlice,35")
    result = csv_query_engine.order(data, 'name', 'asc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Alice', 'age': '35'}, {'name': 'Bob', 'age': '25'}]  # Stable sorting
    assert result == expected

def test_ordering_rejected_if_direction_invalid():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(Exception, match="asc"):
        csv_query_engine.order(data, 'age', 'sideways')

def test_chained_operations_order():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(data, 1).filter(data, 'age', '>', '26')
    expected = [{'name': 'Alice', 'age': '30'}]  # AC-6.1
    assert result == expected

def test_invalid_column_name_rejected():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(Exception) as exc:
        csv_query_engine.filter(data, 'height', '=', '5.5')
    assert str(exc.value) == "unknown column: height"  # AC-6.2

def test_limit_records():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(data, 1)
    expected = [{'name': 'Alice', 'age': '30'}]  # AC-5.1
    assert result == expected

def test_limit_larger_than_records():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(data, 5)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]  # AC-5.2
    assert result == expected

def test_limit_zero_yields_empty_result():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(data, 0)
    expected = []  # AC-5.3
    assert result == expected

def test_limit_negative_rejected():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(Exception, match="non-negative"):
        csv_query_engine.limit(data, -1)

def test_counting_records():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.count(data)
    expected = 2  # AC-5.5
    assert result == expected

def test_counting_filtered_records():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    filtered_data = csv_query_engine.filter(data, 'age', '>', '26')
    result = csv_query_engine.count(filtered_data)
    expected = 1  # Only Alice matches
    assert result == expected

def test_counting_no_matching_records():
    data = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    filtered_data = csv_query_engine.filter(data, 'age', '<', '25')
    result = csv_query_engine.count(filtered_data)
    expected = 0  # No matches
    assert result == expected

def test_single_record_full_chain():
    data = csv_query_engine.read_csv("name,age\nAlice,30")
    result = csv_query_engine.filter(data, 'age', '>', '25').order('age', 'asc').limit(1).count()
    expected = 1  # Only Alice matches
    assert result == expected

def test_projection_with_spaced_header():
    data = csv_query_engine.read_csv("first name,age\nAlice,30\nBob,25")
    result = csv_query_engine.project(data, ['first name'])
    expected = [{'first name': 'Alice'}, {'first name': 'Bob'}]  # AC-2.1 with spaced header
    assert result == expected

def test_filtering_with_spaced_header():
    data = csv_query_engine.read_csv("first name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(data, 'first name', '=', 'Alice')
    expected = [{'first name': 'Alice', 'age': '30'}]  # AC-3.1 with spaced header
    assert result == expected

def test_ordering_with_spaced_header():
    data = csv_query_engine.read_csv("first name,age\nBob,25\nAlice,30")
    result = csv_query_engine.order(data, 'first name', 'asc')
    expected = [{'first name': 'Alice', 'age': '30'}, {'first name': 'Bob', 'age': '25'}]  # AC-4.3 with spaced header
    assert result == expected