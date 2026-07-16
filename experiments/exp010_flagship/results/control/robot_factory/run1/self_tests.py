import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot

# Test suite for Build-a-robot quoting and purchasing

# US-1: Registering a healthy supplier pool
def test_register_suppliers_rejects_fewer_than_three_suppliers():
    with pytest.raises(ValueError) as excinfo:
        register_suppliers([("Supplier A", {"head": {"standard vision": 10}})])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 1"

def test_register_suppliers_rejects_duplicate_supplier_names():
    with pytest.raises(ValueError) as excinfo:
        register_suppliers([
            ("Supplier A", {"head": {"standard vision": 10}}),
            ("Supplier A", {"body": {"square": 20}})
        ])
    assert str(excinfo.value) == "duplicate supplier name Supplier A"

# US-2: Quoting a robot at the lowest cost
def test_quote_robot_returns_lowest_cost_parts():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}}),
        ("Supplier B", {"head": {"standard vision": 8}, "body": {"square": 25}, "arms": {"hands": 15}}),
        ("Supplier C", {"head": {"infrared vision": 12}, "body": {"round": 30}, "arms": {"pinchers": 18}})
    ]
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    # Expected parts and total price
    expected_parts = [
        {"category": "head", "supplier": "Supplier B", "price": 8},
        {"category": "body", "supplier": "Supplier A", "price": 20},
        {"category": "arms", "supplier": "Supplier A", "price": 15},
        {"category": "movement", "supplier": None, "price": 0},  # No supplier for "wheels"
        {"category": "power", "supplier": None, "price": 0}     # No supplier for "solar"
    ]
    expected_total = 43  # 8 + 20 + 15 + 0 + 0
    assert quote['parts'] == expected_parts
    assert quote['total'] == expected_total

def test_quote_robot_ties_resolved_by_registration_order():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}}),
        ("Supplier B", {"head": {"standard vision": 10}})
    ]
    register_suppliers(suppliers)

    quote = quote_robot({"head": "standard vision"})
    
    # Supplier A should win due to registration order
    expected_part = {"category": "head", "supplier": "Supplier A", "price": 10}
    assert quote['parts'] == [expected_part]
    assert quote['total'] == 10

# US-3: Validating robot configurations
def test_validate_configuration_rejects_missing_part_category():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({
            "head": "standard vision",
            "body": "square",
            "arms": "hands",
            "movement": "wheels",  # Missing power
        })
    assert str(excinfo.value) == "missing part category power"

def test_validate_configuration_rejects_unknown_part_category():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({
            "head": "standard vision",
            "body": "square",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar",
            "extra": "invalid"  # Unknown category
        })
    assert str(excinfo.value) == "unknown part category extra"

def test_validate_configuration_rejects_invalid_option():
    with pytest.raises(ValueError) as excinfo:
        validate_configuration({
            "head": "invalid option",  # Not a recognized option
            "body": "square",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar"
        })
    assert str(excinfo.value) == "invalid head option invalid option"

def test_validate_configuration_rejects_unavailable_option():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"head": {"infrared vision": 15}, "body": {"round": 25}})
    ]
    register_suppliers(suppliers)

    with pytest.raises(ValueError) as excinfo:
        validate_configuration({
            "head": "night vision",  # No supplier carries this option
            "body": "square",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar"
        })
    assert str(excinfo.value) == "no supplier carries night vision"

# US-4: Purchasing robots and tracking supplier orders
def test_purchase_robot_records_orders_correctly():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}}),
        ("Supplier B", {"head": {"standard vision": 8}, "body": {"round": 25}, "arms": {"pinchers": 18}})
    ]
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    purchase = purchase_robot(quote)

    # Check that purchase records the correct order
    expected_orders = [
        {"supplier": "Supplier B", "option": "head", "price": 8},  # Supplier B for head
        {"supplier": "Supplier A", "option": "body", "price": 20},  # Supplier A for body
        {"supplier": "Supplier A", "option": "arms", "price": 15}   # Supplier A for arms
    ]

    for order in purchase['orders']:
        assert order in expected_orders

def test_purchase_robot_fails_to_order_if_no_quote():
    with pytest.raises(ValueError) as excinfo:
        purchase_robot(None)  # No prior quote
    assert str(excinfo.value) == "No quote to purchase"

def test_purchase_robot_records_no_orders_on_quote_only():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}})
    ]
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })

    # Ensure no orders are recorded before purchase
    assert 'orders' not in quote

def test_purchase_robot_rejects_unknown_supplier_for_history():
    with pytest.raises(ValueError) as excinfo:
        purchase_robot({"supplier": "Unknown Supplier"})
    assert str(excinfo.value) == "unknown supplier Unknown Supplier"

# US-5: Stamping unique serial names
def test_robot_serial_names_are_correct_format():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}})
    ]
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    purchase = purchase_robot(quote)
    
    serial_name = purchase['serial_name']
    assert len(serial_name) == 5
    assert serial_name[:2].isupper()  # Check first two characters are uppercase
    assert serial_name[2:].isdigit()  # Check last three characters are digits

def test_serial_names_are_unique():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}})
    ]
    register_suppliers(suppliers)

    serial_names = set()
    
    for _ in range(5):  # Purchase 5 robots to test uniqueness
        quote = quote_robot({
            "head": "standard vision",
            "body": "square",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar"
        })
        purchase = purchase_robot(quote)
        serial_names.add(purchase['serial_name'])

    assert len(serial_names) == 5  # All names should be unique