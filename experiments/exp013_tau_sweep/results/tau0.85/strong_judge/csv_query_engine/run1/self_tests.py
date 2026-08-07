# test_csv_query_engine.py

import pytest
from solution import csv_query_engine

def test_read_csv_text_into_records():
    # AC-1.1
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.2
    csv_text = "name,age"
    expected = []
    assert csv_query_engine.read_csv(csv_text) == expected
    # Filtering and counting should also yield empty results
    assert csv_query_engine.filter(expected, 'age', '>', '20') == []
    assert csv_query_engine.count(expected) == 0
    assert csv_query_engine.project(expected, ['name']) == []

    # AC-1.3
    csv_text = 'name,age\n"Smith, John",30'
    expected = [{'name': 'Smith, John', 'age': '30'}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.4
    csv_text = "First Name, Age\nAlice,30"
    expected = [{'First Name': 'Alice', 'Age': '30'}]
    assert csv_query_engine.read_csv(csv_text) == expected
    # Test using header with spaces in filtering
    assert csv_query_engine.filter(expected, 'First Name', '=', 'Alice') == expected
    assert csv_query_engine.project(expected, ['First Name']) == expected

    # AC-1.5
    csv_text = "\n"
    with pytest.raises(ValueError) as exc:
        csv_query_engine.read_csv(csv_text)
    assert str(exc.value) == "CSV text must include a header row"

def test_choose_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-2.1
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert csv_query_engine.project(records, ['name']) == expected

    # AC-2.2
    expected = [{'age': '30', 'name': 'Alice'}, {'age': '25', 'name': 'Bob'}]
    assert list(csv_query_engine.project(records, ['age', 'name'])[0].keys()) == ['age', 'name']
    
    # AC-2.3
    projected = csv_query_engine.project(records, ['name', 'age'])
    filtered = csv_query_engine.filter(projected, 'age', '>=', '25')
    ordered = csv_query_engine.order(filtered, 'name', 'asc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert ordered == expected

def test_filter_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)

    # AC-3.1
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'name', '=', 'Alice') == expected

    # AC-3.1 (Inequality)
    expected_inequality = [{'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.filter(records, 'name', '!=', 'Alice') == expected_inequality

    # AC-3.2
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.filter(records, 'age', '>', '20') == expected

    # AC-3.3
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.filter(records, 'age', '<=', '35') == expected

    # AC-3.4
    expected = [{'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.filter(records, 'age', '=', '25') == expected

    # AC-3.5
    with pytest.raises(ValueError, match="unknown operator"):
        csv_query_engine.filter(records, 'age', 'invalid', '25')

    # AC-3.6: Testing mixed numeric and non-numeric comparison
    assert csv_query_engine.filter(records, 'age', '>', '29') == [{'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.filter(records, 'age', '<', '30') == [{'name': 'Bob', 'age': '25'}]

    # Test for textual fallback
    assert csv_query_engine.filter(records, 'age', '>', '25') == [{'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]

def test_order_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35\nDavid,25"
    records = csv_query_engine.read_csv(csv_text)

    # AC-4.1: Numeric order with stable ties
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'David', 'age': '25'}, {'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.order(records, 'age', 'asc') == expected

    # AC-4.2
    expected = [{'name': 'Charlie', 'age': '35'}, {'name': 'Alice', 'age': '30'}, {'name': 'David', 'age': '25'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.order(records, 'age', 'desc') == expected

    # AC-4.3: Test stable ties with text
    records_with_ties = "name,age\nAlice,30\nBob,25\nCharlie,30\nDavid,25"
    records = csv_query_engine.read_csv(records_with_ties)
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'David', 'age': '25'}, {'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '30'}]
    assert csv_query_engine.order(records, 'age', 'asc') == expected

    # AC-4.4
    with pytest.raises(ValueError, match="asc"):
        csv_query_engine.order(records, 'age', 'invalid')

def test_limit_and_count():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)

    # AC-5.1
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.limit(records, 2) == expected

    # AC-5.2
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.limit(records, 5) == expected

    # AC-5.3
    expected = []
    assert csv_query_engine.limit(records, 0) == expected

    # AC-5.4
    with pytest.raises(ValueError, match="non-negative"):
        csv_query_engine.limit(records, -1)

    # AC-5.5
    assert csv_query_engine.count(records) == 3
    assert csv_query_engine.count(csv_query_engine.filter(records, 'age', '>', '30')) == 0
    assert csv_query_engine.count(csv_query_engine.filter(records, 'age', '<=', '30')) == 2  # Alice and Bob

def test_compose_queries_predictably():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)

    # AC-6.1
    limited = csv_query_engine.limit(records, 2)
    filtered = csv_query_engine.filter(limited, 'age', '>', '25')
    expected = [{'name': 'Alice', 'age': '30'}]
    assert filtered == expected

    # AC-6.1 (Contrasting order)
    filtered_first = csv_query_engine.filter(records, 'age', '>', '25')
    limited_first = csv_query_engine.limit(filtered_first, 2)
    assert limited_first == [{'name': 'Charlie', 'age': '35'}, {'name': 'Alice', 'age': '30'}]

    # AC-6.2
    with pytest.raises(ValueError, match="unknown column unknown_column"):
        csv_query_engine.filter(records, 'unknown_column', '=', 'value')

    # AC-6.2 (Projection)
    with pytest.raises(ValueError, match="unknown column unknown_column"):
        csv_query_engine.project(records, ['name', 'unknown_column'])

    # AC-6.2 (Ordering)
    with pytest.raises(ValueError, match="unknown column unknown_column"):
        csv_query_engine.order(records, 'unknown_column', 'asc')

    # AC-6.3
    single_record = csv_query_engine.read_csv("name,age\nAlice,30")
    filtered = csv_query_engine.filter(single_record, 'age', '>=', '30')
    ordered = csv_query_engine.order(filtered, 'name', 'asc')
    limited = csv_query_engine.limit(ordered, 1)
    assert limited == [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.count(limited) == 1