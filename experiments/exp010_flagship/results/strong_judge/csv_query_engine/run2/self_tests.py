from solution import csv_query_engine
import pytest

def test_read_csv_into_records():
    # AC-1.1
    csv_text = "name,age\nAlice,30\nBob,25"
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.2
    csv_text = "name,age\n"
    expected = []
    assert csv_query_engine.read_csv(csv_text) == expected
    assert csv_query_engine.count(csv_text) == 0  # Ensure count works on empty data
    assert csv_query_engine.filter(expected, "age", "30") == []  # Ensure filtering works

    # AC-1.3
    csv_text = 'name,description\n"Smith, John","Engineer"'
    expected = [{"name": "Smith, John", "description": "Engineer"}]
    assert csv_query_engine.read_csv(csv_text) == expected

    # AC-1.4
    csv_text = "first name,last name,age\nAlice,Smith,30\nBob,Johnson,25"
    expected = [{"first name": "Alice", "last name": "Smith", "age": "30"}, 
                {"first name": "Bob", "last name": "Johnson", "age": "25"}]
    assert csv_query_engine.read_csv(csv_text) == expected
    
    # Test filtering with spaced headers
    assert csv_query_engine.filter(expected, "first name", "Alice") == [{"first name": "Alice", "last name": "Smith", "age": "30"}]

    # AC-1.5
    csv_text = ""
    with pytest.raises(ValueError, match="^CSV text must include a header row$"):
        csv_query_engine.read_csv(csv_text)

def test_choose_columns():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)

    # AC-2.1
    expected = [{"name": "Alice"}, {"name": "Bob"}]
    assert csv_query_engine.project(records, ["name"]) == expected

    # AC-2.2
    expected = [{"age": "30"}, {"age": "25"}]
    assert csv_query_engine.project(records, ["age"]) == expected

    # AC-2.2 - Test multi-column projection order
    expected = [{"age": "30", "name": "Alice"}, {"age": "25", "name": "Bob"}]
    assert csv_query_engine.project(records, ["age", "name"]) == expected

    # AC-2.3
    expected = [{"name": "Bob", "age": "25"}]
    assert csv_query_engine.project(csv_query_engine.filter(records, "age", "25"), ["name", "age"]) == expected

def test_filter_rows():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)

    # AC-3.1
    expected = [{"name": "Alice", "age": "30"}]
    assert csv_query_engine.filter(records, "age", "30") == expected

    # AC-3.1 (inequality)
    expected = [{"name": "Bob", "age": "25"}]
    assert csv_query_engine.filter(records, "age", "25", operator="!=") == expected

    # AC-3.2 - Test numeric ordering
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    assert csv_query_engine.order(records, "age", "asc") == expected

    # AC-3.3
    expected = [{"name": "Alice", "age": "30"}]
    assert csv_query_engine.filter(records, "age", 30, operator=">=") == expected  # Using numeric comparison

    # AC-3.4
    expected = [{"name": "Alice", "age": "30"}]
    assert csv_query_engine.filter(records, "age", 30) == expected  # Numeric comparison

    # AC-3.5
    with pytest.raises(ValueError, match="unknown operator"):
        csv_query_engine.filter(records, "age", "30", operator="unknown")

    # AC-3.6 - Example of one numeric side textual fallback comparison
    expected = [{"name": "Alice", "age": "30"}]
    assert csv_query_engine.filter(records, "age", "25", operator="<") == expected  # Textual fallback

def test_order_rows():
    csv_text = "name,age\nAlice,30\nBob,25\nCharlie,35"
    records = csv_query_engine.read_csv(csv_text)

    # AC-4.1
    expected = [{"name": "Bob", "age": "25"}, {"name": "Alice", "age": "30"}, {"name": "Charlie", "age": "35"}]
    assert csv_query_engine.order(records, "age", "asc") == expected

    # AC-4.2
    expected = [{"name": "Charlie", "age": "35"}, {"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    assert csv_query_engine.order(records, "age", "desc") == expected

    # AC-4.3 - Test stable sorting with tied records
    csv_text = "name,age\nCharlie,35\nAlice,30\nBob,25\nAlice,35"
    records = csv_query_engine.read_csv(csv_text)
    expected = [{"name": "Alice", "age": "30"}, {"name": "Alice", "age": "35"}, {"name": "Bob", "age": "25"}, {"name": "Charlie", "age": "35"}]
    assert csv_query_engine.order(records, "age", "asc") == expected

    # AC-4.4
    with pytest.raises(ValueError, match="accepted direction is 'asc' or 'desc'"):
        csv_query_engine.order(records, "age", "invalid")

def test_limit_and_count():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)

    # AC-5.1
    expected = [{"name": "Alice", "age": "30"}]
    assert csv_query_engine.limit(records, 1) == expected

    # AC-5.2
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    assert csv_query_engine.limit(records, 10) == expected

    # AC-5.3
    expected = []
    assert csv_query_engine.limit(records, 0) == expected

    # AC-5.4
    with pytest.raises(ValueError, match="non-negative"):
        csv_query_engine.limit(records, -1)

    # AC-5.5
    assert csv_query_engine.count(records) == 2  # Total records

    # Test count on a filtered subset
    filtered_records = csv_query_engine.filter(records, "age", "25")
    assert csv_query_engine.count(filtered_records) == 1  # Only Bob matches

    # Test count on zero matching records
    empty_filtered = csv_query_engine.filter(records, "age", "100")
    assert csv_query_engine.count(empty_filtered) == 0  # No matches

def test_compose_queries():
    csv_text = "name,age\nAlice,30\nBob,25"
    records = csv_query_engine.read_csv(csv_text)

    # AC-6.1
    assert csv_query_engine.limit(csv_query_engine.filter(records, "age", "25"), 1) == [{"name": "Bob", "age": "25"}]
    assert csv_query_engine.filter(csv_query_engine.limit(records, 1), "age", "25") == []  # Limit first yields different results

    # AC-6.2 - Test unknown column in filter
    with pytest.raises(ValueError, match="unknown column unknown"):
        csv_query_engine.filter(records, "unknown", "25")

    # Test unknown column in project
    with pytest.raises(ValueError, match="unknown column unknown"):
        csv_query_engine.project(records, ["unknown"])

    # Test unknown column in order
    with pytest.raises(ValueError, match="unknown column unknown"):
        csv_query_engine.order(records, "unknown", "asc")

    # AC-6.3 - Full chain on a single record
    single_record_csv = "name,age\nAlice,30"
    single_record = csv_query_engine.read_csv(single_record_csv)
    assert csv_query_engine.count(csv_query_engine.limit(csv_query_engine.order(csv_query_engine.filter(single_record, "name", "Alice"), "age", "asc"), 1)) == 1