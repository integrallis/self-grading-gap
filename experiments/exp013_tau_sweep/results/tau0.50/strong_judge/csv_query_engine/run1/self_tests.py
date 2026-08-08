import pytest
from solution import read_csv

def test_read_csv_text_into_records():
    # AC-1.1
    result = read_csv("name,age\nAlice,30\nBob,25")
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert result == expected

    # AC-1.2
    result = read_csv("name,age\n")
    expected = []
    assert result == expected
    assert len(result) == 0  # count should be zero
    assert read_csv("name,age\n").filter('name', '=', 'Alice') == []  # filtering still works

    # AC-1.3
    result = read_csv("name,description\nItem1,\"A, B, C\"\nItem2,\"D, E\"")
    expected = [{'name': 'Item1', 'description': 'A, B, C'}, {'name': 'Item2', 'description': 'D, E'}]
    assert result == expected

    # AC-1.4
    result = read_csv("name with space,age with space\nAlice,30\nBob,25")
    expected = [{'name with space': 'Alice', 'age with space': '30'}, {'name with space': 'Bob', 'age with space': '25'}]
    assert result == expected

    # AC-1.5
    with pytest.raises(Exception, match=r"^CSV text must include a header row$"):
        read_csv("")

def test_choose_columns():
    data = read_csv("name,age\nAlice,30\nBob,25")

    # AC-2.1
    result = data.project(['name'])
    expected = [{'name': 'Alice'}, {'name': 'Bob'}]
    assert result == expected

    # AC-2.2
    result = data.project(['age', 'name'])
    expected = [{'age': '30', 'name': 'Alice'}, {'age': '25', 'name': 'Bob'}]
    assert list(result[0].keys()) == ['age', 'name']  # verify order
    assert result == expected

    # AC-2.3
    result = data.project(['name']).filter('name', '=', 'Alice')
    expected = [{'name': 'Alice'}]
    assert result == expected

    # Test ordering after projection
    result = data.project(['name', 'age']).order_by('age', 'asc')
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}]
    assert result == expected

def test_filter_rows():
    data = read_csv("name,age\nAlice,30\nBob,25\nCharlie,35")

    # AC-3.1
    result = data.filter('name', '=', 'Alice')
    expected = [{'name': 'Alice', 'age': '30'}]
    assert result == expected

    # AC-3.1 (inequality)
    result = data.filter('name', '!=', 'Alice')
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert result == expected

    # AC-3.2
    result = data.filter('age', '>', '28')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]
    assert result == expected

    # AC-3.3
    result = data.filter('age', '<', '30')
    expected = [{'name': 'Bob', 'age': '25'}]
    assert result == expected

    # AC-3.3 (inclusive boundary)
    result = data.filter('age', '<=', '30')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert result == expected

    # AC-3.4 (testing numeric equality)
    result = data.filter('age', '=', '30')
    expected = [{'name': 'Alice', 'age': '30'}]
    assert result == expected

    # Numeric equality test distinguishing numeric from textual
    result = data.filter('age', '=', '30.0')
    assert result == expected  # '30' and '30.0' should be equal numerically

    # AC-3.5
    with pytest.raises(Exception, match="unknown operator"):
        data.filter('age', 'invalid_op', '30')

    # AC-3.6 (testing mixed numeric/text ordering)
    result = data.filter('name', '>', 'Alice')
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]  # Lexical comparison
    assert result == expected

def test_order_rows():
    data = read_csv("name,age\nAlice,30\nBob,25\nCharlie,35")

    # AC-4.1
    result = data.order_by('age', 'asc')
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Alice', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]
    assert result == expected

    # AC-4.1 (stable ties)
    data_tie = read_csv("name,age\nAlice,30\nBob,30\nCharlie,35")
    result = data_tie.order_by('age', 'asc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '30'}, {'name': 'Charlie', 'age': '35'}]
    assert result == expected

    # AC-4.1 (ascending numeric ordering)
    data_order_test = read_csv("name,age\nItem,9\nItem,10\nItem,100")
    result = data_order_test.order_by('age', 'asc')
    expected = [{'name': 'Item', 'age': '9'}, {'name': 'Item', 'age': '10'}, {'name': 'Item', 'age': '100'}]
    assert result == expected

    # AC-4.2
    result = data.order_by('age', 'desc')
    expected = [{'name': 'Charlie', 'age': '35'}, {'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert result == expected

    # AC-4.3
    result = data.order_by('name', 'asc')
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert result == expected

    # AC-4.3 (stable ties)
    data_stable_tie = read_csv("name,age\nBob,25\nAlice,30\nCharlie,25")
    result = data_stable_tie.order_by('age', 'asc')
    expected = [{'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '25'}, {'name': 'Alice', 'age': '30'}]
    assert result == expected

    # AC-4.4
    with pytest.raises(Exception, match="asc"):
        data.order_by('age', 'invalid_direction')

def test_limit_and_count():
    data = read_csv("name,age\nAlice,30\nBob,25\nCharlie,35")

    # AC-5.1
    result = data.limit(2)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]
    assert result == expected

    # AC-5.2
    result = data.limit(10)
    expected = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}, {'name': 'Charlie', 'age': '35'}]
    assert result == expected

    # AC-5.3
    result = data.limit(0)
    expected = []
    assert result == expected

    # AC-5.4
    with pytest.raises(Exception, match="non-negative"):
        data.limit(-1)

    # AC-5.5
    assert len(data) == 3
    assert len(data.filter('age', '>', '30')) == 1
    assert len(data.filter('age', '>', '99')) == 0

def test_compose_queries_predictably():
    data = read_csv("name,age\nAlice,30\nBob,25\nCharlie,35")

    # AC-6.1
    result = data.limit(2).filter('age', '>', '25')
    expected = [{'name': 'Alice', 'age': '30'}]
    assert result == expected

    # AC-6.2
    with pytest.raises(Exception, match="unknown column"):
        data.filter('non_existing_column', '=', 'value')

    # AC-6.3
    result = data.limit(1).filter('name', '=', 'Alice').order_by('age', 'asc').count()
    expected_count = 1
    assert result == expected_count