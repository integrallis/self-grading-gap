import pytest
from solution import csv_query_engine

def test_read_csv_into_records():
    # AC-1.1
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.read_csv(csv_text) == expected
    
    # AC-1.2
    csv_text = "name,age\n"
    expected = []
    assert csv_query_engine.read_csv(csv_text) == expected
    
    # AC-1.3
    csv_text = "name,description\n\"Alice, the engineer\",30\nBob,25"
    expected = [{'name': 'Alice, the engineer', 'description': '30'}, {'name': 'Bob', 'description': '25'}]
    assert csv_query_engine.read_csv(csv_text) == expected
    
    # AC-1.4
    csv_text = "name,age with spaces\nAlice,30\nBob,25"
    expected = [{'name': 'Alice', 'age with spaces': '30'}, {'name': 'Bob', 'age with spaces': '25'}]
    assert csv_query_engine.read_csv(csv_text) == expected
    
    # AC-1.5
    csv_text = "age,30\nBob,25"
    with pytest.raises(ValueError, match="CSV text must include a header row"):
        csv_query_engine.read_csv(csv_text)

def test_choose_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-2.1
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert csv_query_engine.project(records, ['name']) == expected
    
    # AC-2.2
    expected = [{'age': '30', 'name': 'Alice'}, {'age': '25', 'name': 'Bob'}]
    assert csv_query_engine.project(records, ['name', 'age']) == expected
    
    # AC-2.3
    filtered = csv_query_engine.filter(records, 'age', '>', '20')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.project(filtered, ['name']) == expected

def test_filter_rows():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-3.1
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'name', '=', 'Alice') == expected
    assert csv_query_engine.filter(records, 'name', '!=', 'Alice') == [{'name': 'Bob', 'age': '25'}]
    
    # AC-3.2
    assert csv_query_engine.filter(records, 'age', '>', '20') == [{'name': 'Alice', 'age': '30'}]
    
    # AC-3.3
    assert csv_query_engine.filter(records, 'age', '<', '30') == [{'name': 'Bob', 'age': '25'}]
    
    # AC-3.4
    expected = [{'name': 'Alice', 'age': '30'}]
    assert csv_query_engine.filter(records, 'age', '=', '30') == expected
    
    # AC-3.5
    with pytest.raises(ValueError, match="unknown operator"):
        csv_query_engine.filter(records, 'age', 'invalid', '30')
    
    # AC-3.6
    assert csv_query_engine.filter(records, 'name', '=', 'Alice') == expected

def test_order_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-4.1
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.order(records, 'age', 'asc') == expected
    
    # AC-4.2
    expected = [{'name': 'Charlie', 'age': '35'}, {'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert csv_query_engine.order(records, 'age', 'desc') == expected
    
    # AC-4.3
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert csv_query_engine.order(records, 'name', 'asc') == expected
    
    # AC-4.4
    with pytest.raises(ValueError, match="accepted 'asc' direction"):
        csv_query_engine.order(records, 'age', 'invalid')

def test_limit_and_count():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-5.1
    assert csv_query_engine.limit(records, 2) == [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    
    # AC-5.2
    assert csv_query_engine.limit(records, 10) == [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    
    # AC-5.3
    assert csv_query_engine.limit(records, 0) == []
    
    # AC-5.4
    with pytest.raises(ValueError, match="non-negative"):
        csv_query_engine.limit(records, -1)
    
    # AC-5.5
    assert csv_query_engine.count(records) == 3
    assert csv_query_engine.count(csv_query_engine.filter(records, 'age', '>', '30')) == 1

def test_compose_queries_predictably():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)
    
    # AC-6.1
    assert csv_query_engine.limit(csv_query_engine.filter(records, 'age', '>', '20'), 1) == [{'name': 'Alice', 'age': '30'}]
    
    # AC-6.2
    with pytest.raises(ValueError, match="unknown column"):
        csv_query_engine.filter(records, 'unknown_column', '=', 'value')
    
    # AC-6.3
    assert csv_query_engine.count(csv_query_engine.filter(records, 'name', '=', 'Alice')) == 1