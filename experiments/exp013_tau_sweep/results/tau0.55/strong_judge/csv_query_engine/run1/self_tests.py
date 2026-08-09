import pytest
from solution import *  # Assuming all functions are defined in the solution package

def test_read_csv_into_records():
    # Test AC-1.1: Every data line becomes one record mapping each header name to that line's value, with values kept as text.
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert read_csv(csv_text) == expected

    # Test AC-1.2: CSV with only a header line yields no records
    csv_text = "name,age\n"
    expected = []
    assert read_csv(csv_text) == expected
    assert count(read_csv(csv_text)) == 0
    projected = project(read_csv(csv_text), ["name"])
    assert projected == []

    # Test AC-1.3: A quoted field keeps an embedded comma as part of a single value
    csv_text = "name,age\n\"Alice, A\",30\nBob,25"
    expected = [
        {"name": "Alice, A", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert read_csv(csv_text) == expected

    # Test AC-1.4: Header names containing spaces are usable in every operation
    csv_text = "first name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)
    assert project(records, ["first name"]) == [{"first name": "Alice"}, {"first name": "Bob"}]
    assert filter(records, "first name", "=", "Alice") == [{"first name": "Alice", "age": "30"}]
    assert order(records, "first name", "asc") == [
        {"first name": "Alice", "age": "30"},
        {"first name": "Bob", "age": "25"},
    ]

    # Test AC-1.5: CSV text without a header line is rejected
    csv_text = "Alice,30\nBob,25"
    with pytest.raises(ValueError) as excinfo:
        read_csv(csv_text)
    assert str(excinfo.value) == "CSV text must include a header row"

    # Test filtering on an empty header-only CSV
    csv_text = "name,age\n"
    filtered = filter(read_csv(csv_text), "age", ">", "20")
    assert filtered == []

def test_choose_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)

    # Test AC-2.1: Projection keeps only the requested columns for every record
    projected = project(records, ["name"])
    expected = [
        {"name": "Alice"},
        {"name": "Bob"}
    ]
    assert projected == expected

    # Test AC-2.2: Projected columns appear in the order they were requested
    projected = project(records, ["age", "name"])
    expected_keys = ["age", "name"]
    assert list(projected[0].keys()) == expected_keys
    assert list(projected[1].keys()) == expected_keys

    # Test AC-2.3: A projected query can still be filtered and ordered by its remaining columns
    projected = project(records, ["name", "age"])
    filtered = filter(projected, "age", ">", "25")
    ordered = order(filtered, "age", "asc")
    expected = [
        {"name": "Alice", "age": "30"}
    ]
    assert ordered == expected

def test_filter_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,30"
    records = read_csv(csv_text)

    # Test AC-3.1: Equality (=) keeps exactly the records whose column value matches
    filtered = filter(records, "age", "=", "30")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Charlie", "age": "30"}]
    assert filtered == expected

    # Test AC-3.1: Inequality (!=) keeps exactly the records whose column value differs
    filtered = filter(records, "age", "!=", "30")
    expected = [{"name": "Bob", "age": "25"}]
    assert filtered == expected

    # Test AC-3.2: Numeric comparisons
    filtered = filter(records, "age", ">", "26")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Charlie", "age": "30"}]
    assert filtered == expected

    # Test AC-3.3: Boundary semantics
    filtered = filter(records, "age", ">", "30")
    expected = []
    assert filtered == expected

    filtered = filter(records, "age", "<=", "30")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}, {"name": "Charlie", "age": "30"}]
    assert filtered == expected

    # Test AC-3.4: Equality against a numeric comparison value matches records by numeric value
    filtered = filter(records, "age", "=", "25")
    expected = [{"name": "Bob", "age": "25"}]
    assert filtered == expected

    # Test AC-3.5: Operators other than =, !=, >, <, >=, <= are rejected
    with pytest.raises(ValueError) as excinfo:
        filter(records, "age", "unknown", "25")
    assert "unknown operator" in str(excinfo.value)

    # Test AC-3.6: When only one side is numeric, fall back to textual ordering
    filtered = filter(records, "age", "=", "Alice")
    expected = []
    assert filtered == expected

    # Test AC-3.4: Numeric equality using numerically equal but textually different values
    filtered = filter(records, "age", "=", "02")
    expected = []  # No match since "30" != "02" as numbers
    assert filtered == expected

def test_order_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = read_csv(csv_text)

    # Test AC-4.1: Ascending order on a numeric column sorts by numeric value
    ordered = order(records, "age", "asc")
    expected = [
        {"name": "Bob", "age": "25"},
        {"name": "Alice", "age": "30"},
        {"name": "Charlie", "age": "35"}
    ]
    assert ordered == expected

    # Test AC-4.1: Numeric ordering with ties
    csv_text = "name,age\nAlice,30\nBob,30\nCharlie,25"
    records = read_csv(csv_text)
    ordered = order(records, "age", "asc")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "30"},
        {"name": "Charlie", "age": "25"},
    ]
    assert ordered == expected

    # Test AC-4.2: Descending order sorts from highest to lowest
    ordered = order(records, "age", "desc")
    expected = [
        {"name": "Charlie", "age": "35"},
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]
    assert ordered == expected

    # Test AC-4.3: Ordering on a textual column sorts alphabetically
    ordered = order(records, "name", "asc")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
        {"name": "Charlie", "age": "35"}
    ]
    assert ordered == expected

    # Test AC-4.4: Only "asc" and "desc" are accepted directions
    with pytest.raises(ValueError) as excinfo:
        order(records, "age", "unknown")
    assert "unknown direction" in str(excinfo.value)

    # Test AC-4.3: Stable ordering on ties
    csv_text = "name,age\nAlice,30\nBob,30\nCharlie,25"
    records = read_csv(csv_text)
    ordered = order(records, "age", "asc")
    expected = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "30"},
        {"name": "Charlie", "age": "25"},
    ]
    assert ordered == expected

def test_limit_and_count():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)

    # Test AC-5.1: A limit keeps only the first n records
    limited = limit(records, 1)
    expected = [{"name": "Alice", "age": "30"}]
    assert limited == expected

    # Test AC-5.2: A limit larger than the number of records returns everything
    limited = limit(records, 3)
    expected = records
    assert limited == expected

    # Test AC-5.3: A limit of zero yields an empty result
    limited = limit(records, 0)
    expected = []
    assert limited == expected

    # Test AC-5.4: A negative limit is rejected
    with pytest.raises(ValueError) as excinfo:
        limit(records, -1)
    assert "non-negative" in str(excinfo.value)

    # Test AC-5.5: Counting reports how many records match
    count_result = count(records)
    expected = 2
    assert count_result == expected

    filtered = filter(records, "age", ">", "20")
    count_result = count(filtered)
    expected = 2
    assert count_result == expected

    filtered = filter(records, "age", "<", "20")
    count_result = count(filtered)
    expected = 0
    assert count_result == expected

def test_compose_queries():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = read_csv(csv_text)

    # Test AC-6.1: Operations apply in call order
    limited = limit(records, 1)
    filtered = filter(limited, "age", ">", "25")
    expected = []  # The only record is "Alice", which does not match the filter
    assert filtered == expected

    # Test with filter first
    filtered = filter(records, "age", ">", "25")
    limited = limit(filtered, 1)
    expected = [{"name": "Alice", "age": "30"}]  # Now "Alice" matches the filter
    assert limited == expected

    # Test AC-6.2: Projecting, filtering or ordering by a column absent from the header is rejected
    with pytest.raises(ValueError) as excinfo:
        project(records, ["nonexistent"])
    assert "unknown column nonexistent" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        filter(records, "nonexistent", "=", "30")
    assert "unknown column nonexistent" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        order(records, "nonexistent", "asc")
    assert "unknown column nonexistent" in str(excinfo.value)

    # Test AC-6.3: The full chain works on a dataset of a single record
    single_record = [{"name": "Alice", "age": "30"}]
    filtered = filter(single_record, "age", "=", "30")
    ordered = order(filtered, "name", "asc")
    limited = limit(ordered, 1)
    count_result = count(limited)
    expected = 1
    assert count_result == expected