import pytest
from solution import csv_query_engine

# US-1: Read CSV text into records
def test_empty_csv():
    with pytest.raises(ValueError) as exc:
        csv_query_engine.read_csv("")  # AC-1.5
    assert str(exc.value) == "CSV text must include a header row"  # exact message

def test_csv_with_header_only():
    result = csv_query_engine.read_csv("name,age")
    assert result == []  # AC-1.2

def test_csv_with_records():
    result = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]  # AC-1.1
    assert result == expected

def test_quoted_field_with_comma():
    result = csv_query_engine.read_csv("name,age\n\"Alice, the Brave\",30")
    expected = [{"name": "Alice, the Brave", "age": "30"}]  # AC-1.3
    assert result == expected

def test_header_with_spaces():
    result = csv_query_engine.read_csv("first name,age\nAlice,30")
    expected = [{"first name": "Alice", "age": "30"}]  # AC-1.4
    assert result == expected

# Additional tests for header-only count and filtering
def test_count_records_in_header_only_csv():
    result = csv_query_engine.read_csv("name,age")
    count = csv_query_engine.count(result)
    assert count == 0  # AC-5.5

def test_filtering_in_header_only_csv():
    result = csv_query_engine.read_csv("name,age")
    filtered = csv_query_engine.filter(result, "name", "Alice", operator="=")
    assert filtered == []  # AC-3.1

def test_projecting_in_header_only_csv():
    result = csv_query_engine.read_csv("name,age")
    projected = csv_query_engine.project(result, ["name"])
    assert projected == []  # AC-2.1


# US-2: Choose columns
def test_project_columns():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.project(records, ["name"])
    expected = [{"name": "Alice"}, {"name": "Bob"}]  # AC-2.1
    assert result == expected

def test_project_columns_order():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.project(records, ["age", "name"])
    assert list(result[0].keys()) == ["age", "name"]  # AC-2.2
    expected = [{"age": "30", "name": "Alice"}, {"age": "25", "name": "Bob"}]
    assert result == expected

def test_projected_query_can_filter():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    projected = csv_query_engine.project(records, ["name"])
    result = csv_query_engine.filter(projected, "name", "Alice", operator="=")
    expected = [{"name": "Alice"}]  # AC-2.3
    assert result == expected

def test_projected_query_can_order():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    projected = csv_query_engine.project(records, ["age", "name"])
    result = csv_query_engine.order(projected, "age", direction="asc")
    expected = [{"age": "25", "name": "Bob"}, {"age": "30", "name": "Alice"}]  # AC-2.3
    assert result == expected


# US-3: Filter rows
def test_filter_equals():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "30", operator="=")
    expected = [{"name": "Alice", "age": "30"}]  # AC-3.1
    assert result == expected

def test_filter_not_equals():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "25", operator="!=")
    expected = [{"name": "Alice", "age": "30"}]  # AC-3.1
    assert result == expected

def test_numeric_comparison_greater_than():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "26", operator=">")
    expected = [{"name": "Alice", "age": "30"}]  # AC-3.2, AC-3.3
    assert result == expected

def test_numeric_comparison_less_than():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "30", operator="<")
    expected = [{"name": "Bob", "age": "25"}]  # AC-3.3
    assert result == expected

def test_numeric_comparison_equals_numeric():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "30", operator="=")
    expected = [{"name": "Alice", "age": "30"}]  # AC-3.4
    assert result == expected

def test_numeric_comparison_equals_textually_different():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "30.0", operator="=")
    expected = [{"name": "Alice", "age": "30"}]  # AC-3.4
    assert result == expected

def test_unknown_operator_raises_error():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(ValueError) as exc:
        csv_query_engine.filter(records, "age", "30", operator="unknown")  # AC-3.5
    assert "unknown operator" in str(exc.value)

def test_comparison_with_non_numeric_value():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "30", operator="<")
    expected = [{"name": "Bob", "age": "25"}]  # AC-3.6
    assert result == expected

def test_numeric_comparison_one_side_textual():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "Twenty Five", operator="<")
    expected = [{"name": "Bob", "age": "25"}]  # AC-3.6
    assert result == expected

def test_boundary_greater_than_equals():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "30", operator=">=")
    expected = [{"name": "Alice", "age": "30"}]  # AC-3.3
    assert result == expected

def test_boundary_less_than_equals():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.filter(records, "age", "25", operator="<=")
    expected = [{"name": "Bob", "age": "25"}, {"name": "Alice", "age": "30"}]  # AC-3.3
    assert result == expected

def test_filter_preserves_input_order():
    records = csv_query_engine.read_csv("name,age\nBob,25\nAlice,30\nCharlie,25")
    result = csv_query_engine.filter(records, "age", "25", operator="=")
    expected = [{"name": "Bob", "age": "25"}, {"name": "Charlie", "age": "25"}]  # AC-3.1
    assert result == expected


# US-4: Order rows
def test_order_ascending():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.order(records, "age", direction="asc")
    expected = [{"name": "Bob", "age": "25"}, {"name": "Alice", "age": "30"}]  # AC-4.1
    assert result == expected

def test_order_numeric_ascending_stable():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25\nCharlie,25")
    result = csv_query_engine.order(records, "age", direction="asc")
    expected = [{"name": "Bob", "age": "25"}, {"name": "Charlie", "age": "25"}, {"name": "Alice", "age": "30"}]  # AC-4.1
    assert result == expected

def test_order_descending():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.order(records, "age", direction="desc")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]  # AC-4.2
    assert result == expected

def test_order_textual_column():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.order(records, "name", direction="asc")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]  # AC-4.3
    assert result == expected

def test_order_numeric_stable_ties():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,30")
    result = csv_query_engine.order(records, "age", direction="asc")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "30"}]  # AC-4.1
    assert result == expected

def test_order_textual_stable_ties():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nAlice,28")
    result = csv_query_engine.order(records, "name", direction="asc")
    expected = [{"name": "Alice", "age": "30"}, {"name": "Alice", "age": "28"}]  # AC-4.3
    assert result == expected

def test_invalid_order_direction_raises_error():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(ValueError) as exc:
        csv_query_engine.order(records, "age", direction="invalid")  # AC-4.4
    assert "accepted" in str(exc.value)


# US-5: Limit and count
def test_limit_records():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(records, 1)
    expected = [{"name": "Alice", "age": "30"}]  # AC-5.1
    assert result == expected

def test_limit_greater_than_number_of_records():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(records, 3)
    expected = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]  # AC-5.2
    assert result == expected

def test_limit_zero_yields_empty_result():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.limit(records, 0)
    expected = []  # AC-5.3
    assert result == expected

def test_negative_limit_raises_error():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(ValueError) as exc:
        csv_query_engine.limit(records, -1)  # AC-5.4
    assert "non-negative" in str(exc.value)

def test_count_records():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    result = csv_query_engine.count(records)
    expected = 2  # AC-5.5
    assert result == expected

def test_count_filtered_records():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    filtered = csv_query_engine.filter(records, "age", "30", operator="=")
    count = csv_query_engine.count(filtered)
    assert count == 1  # AC-5.5

def test_count_zero_matching_records():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    filtered = csv_query_engine.filter(records, "age", "50", operator="=")
    count = csv_query_engine.count(filtered)
    assert count == 0  # AC-5.5


# US-6: Compose queries predictably
def test_operations_apply_in_call_order():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    limited = csv_query_engine.limit(records, 1)
    filtered = csv_query_engine.filter(limited, "name", "Alice", operator="=")
    expected = [{"name": "Alice", "age": "30"}]  # AC-6.1
    assert filtered == expected

def test_limit_before_filter_different_result():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    limited = csv_query_engine.limit(records, 1)
    filtered = csv_query_engine.filter(limited, "age", "25", operator="=")
    expected = []  # AC-6.1, limiting first excludes Bob
    assert filtered == expected

def test_projecting_unknown_column_raises_error():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(ValueError) as exc:
        csv_query_engine.project(records, ["unknown"])  # AC-6.2
    assert "unknown column" in str(exc.value)

def test_filtering_unknown_column_raises_error():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(ValueError) as exc:
        csv_query_engine.filter(records, "unknown", "value", operator="=")  # AC-6.2
    assert "unknown column" in str(exc.value)

def test_ordering_unknown_column_raises_error():
    records = csv_query_engine.read_csv("name,age\nAlice,30\nBob,25")
    with pytest.raises(ValueError) as exc:
        csv_query_engine.order(records, "unknown", direction="asc")  # AC-6.2
    assert "unknown column" in str(exc.value)

def test_single_record_full_chain():
    records = csv_query_engine.read_csv("name,age\nAlice,30")
    projected = csv_query_engine.project(records, ["name"])
    filtered = csv_query_engine.filter(projected, "name", "Alice", operator="=")
    ordered = csv_query_engine.order(filtered, "name", direction="asc")
    limited = csv_query_engine.limit(ordered, 1)
    count = csv_query_engine.count(limited)
    assert count == 1  # AC-6.3