import pytest
from solution import csv_query_engine

def test_read_csv_text_into_records():
    # AC-1.1
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.2
    csv_text = "name,age\n"
    expected = []
    records = csv_query_engine.read_csv(csv_text)
    assert records == expected
    assert csv_query_engine.count(records) == 0
    assert csv_query_engine.project(records, ['name']) == []
    # Filtering an empty header-only CSV should yield empty result
    assert csv_query_engine.filter(records, 'name', '=', 'Alice') == []

    # AC-1.3
    csv_text = '"Product, A","This is a product."'
    expected = [{'Product, A': 'This is a product.'}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.4
    csv_text = "first name,age\nAlice,30\nBob,25"
    expected = [{'first name': 'Alice', 'age': '30'}, {'first name': 'Bob', 'age': '25'}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.5
    csv_text = ""
    with pytest.raises(ValueError, match="^CSV text must include a header row$"):
        csv_query_engine.read_csv(csv_text)  # No header

def test_choose_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-2.1
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert csv_query_engine.project(records, ['name']) == expected
    
    # AC-2.2
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    projected = csv_query_engine.project(records, ['name', 'age'])
    for record, exp in zip(projected, expected):
        assert list(record.items()) == list(exp.items())

    # AC-2.3
    filtered = csv_query_engine.filter(records, 'age', '>', '20')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    projected_filtered = csv_query_engine.project(filtered, ['name', 'age'])
    for record, exp in zip(projected_filtered, expected):
        assert list(record.items()) == list(exp.items())

def test_filter_rows():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-3.1
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'name', '=', 'Alice') == expected
    
    # AC-3.2
    expected = [{'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.filter(records, 'age', '<', '30') == expected

    # AC-3.3
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.filter(records, 'age', '>=', '25') == expected

    # AC-3.4
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'age', '=', '30') == expected

    # AC-3.5
    with pytest.raises(ValueError, match="unknown operator"):
        csv_query_engine.filter(records, 'age', 'invalid', '30')

    # AC-3.6
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'age', '>', '29') == expected
    assert csv_query_engine.filter(records, 'age', '<', '31') == expected

    # Test inequality
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'age', '!=', '25') == expected

    # Test ordering preservation
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25\nCharlie,30")
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '30'}]
    assert csv_query_engine.filter(records, 'age', '=', '30') == expected

def test_order_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,10"
    records = csv_query_engine.read_csv(csv_text)

    # AC-4.1
    expected = [{'name': 'Charlie', 'age': '10'}, {'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.order(records, 'age', 'asc') == expected

    # AC-4.2
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '10'}]
    assert csv_query_engine.order(records, 'age', 'desc') == expected

    # AC-4.3
    csv_text = "name\nBob\nAlice"
    records = csv_query_engine.read_csv(csv_text)
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert csv_query_engine.order(records, 'name', 'asc') == expected

    # AC-4.4
    with pytest.raises(ValueError, match="asc"):
        csv_query_engine.order(records, 'age', 'invalid')

def test_limit_and_count():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,20"
    records = csv_query_engine.read_csv(csv_text)

    # AC-5.1
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.limit(records, 2) == expected

    # AC-5.2
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '20'}]
    assert csv_query_engine.limit(records, 5) == expected

    # AC-5.3
    expected = []
    assert csv_query_engine.limit(records, 0) == expected

    # AC-5.4
    with pytest.raises(ValueError, match="non-negative"):
        csv_query_engine.limit(records, -1)

    # AC-5.5
    expected = 3
    assert csv_query_engine.count(records) == expected

    # Test filtered count
    filtered = csv_query_engine.filter(records, 'age', '>', '20')
    assert csv_query_engine.count(filtered) == 2  # should count Alice and Bob

    # Test count of an empty result
    empty_records = csv_query_engine.read_csv("name,age\n")
    assert csv_query_engine.count(empty_records) == 0

def test_compose_queries_predictably():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)

    # AC-6.1
    limited_then_filtered = csv_query_engine.limit(records, 1)
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(limited_then_filtered, 'age', '>', '20') == expected

    limited_then_filtered = csv_query_engine.filter(records, 'age', '>', '20')
    limited_then_filtered = csv_query_engine.limit(limited_then_filtered, 1)
    assert limited_then_filtered == [{'name': 'Alice', 'age': '30'}]

    # AC-6.2
    with pytest.raises(ValueError, match="unknown column nonexistent"):
        csv_query_engine.filter(records, 'nonexistent', '=', 'value')

    with pytest.raises(ValueError, match="unknown column nonexistent"):
        csv_query_engine.project(records, ['nonexistent'])

    with pytest.raises(ValueError, match="unknown column nonexistent"):
        csv_query_engine.order(records, 'nonexistent', 'asc')

    # AC-6.3
    single_record = [{'name': 'Alice', 'age': '30'}]
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(single_record, 'name', '=', 'Alice') == expected

    # Test filter, order, limit, count on single record
    single_csv = "name,age\nAlice,30"
    single_records = csv_query_engine.read_csv(single_csv)
    filtered = csv_query_engine.filter(single_records, 'age', '>=', '30')
    ordered = csv_query_engine.order(filtered, 'name', 'asc')
    limited = csv_query_engine.limit(ordered, 1)
    assert csv_query_engine.count(limited) == 1