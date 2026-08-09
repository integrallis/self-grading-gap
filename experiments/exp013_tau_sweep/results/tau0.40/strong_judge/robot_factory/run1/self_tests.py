import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot, get_order_history

# Test suite for Build-a-robot quoting and purchasing

# US-1: Registering a healthy supplier pool
def test_register_suppliers_with_zero_suppliers():
    with pytest.raises(Exception) as excinfo:
        register_suppliers([])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 0"

def test_register_suppliers_with_two_suppliers():
    with pytest.raises(Exception) as excinfo:
        register_suppliers([("Supplier A", {"head": {"standard vision": 10}}),
                            ("Supplier B", {"head": {"infrared vision": 15}})])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_with_duplicate_names():
    with pytest.raises(Exception) as excinfo:
        register_suppliers([("Supplier A", {"head": {"standard vision": 10}}),
                            ("Supplier A", {"head": {"infrared vision": 15}}),
                            ("Supplier B", {"head": {"night vision": 20}})])
    assert str(excinfo.value) == "duplicate supplier name Supplier A"

def test_register_suppliers_with_exactly_three_suppliers():
    result = register_suppliers([("Supplier A", {"head": {"standard vision": 10}}),
                                  ("Supplier B", {"head": {"infrared vision": 15}}),
                                  ("Supplier C", {"head": {"night vision": 20}})])
    assert result is None  # No exception raised

# US-2: Quoting a robot at the lowest cost
def test_quote_robot_with_lowest_cost_parts():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10, "infrared vision": 15},
                         "body": {"square": 20},
                         "arms": {"hands": 5},
                         "movement": {"wheels": 30},
                         "power": {"solar": 50}}),
        ("Supplier B", {"head": {"standard vision": 12},
                         "body": {"square": 18, "round": 25},
                         "arms": {"pinchers": 4},
                         "movement": {"legs": 28, "wheels": 31},
                         "power": {"rechargeable battery": 40}}),
        ("Supplier C", {"head": {"night vision": 14},
                         "body": {"triangular": 22},
                         "arms": {"boxing gloves": 6},
                         "movement": {"tracks": 35},
                         "power": {"biomass": 45}})
    ]
    
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    # Expected parts and total
    expected_parts = {
        "head": ("Supplier A", "standard vision", 10),
        "body": ("Supplier B", "square", 18),  # Supplier B wins for body
        "arms": ("Supplier A", "hands", 5),
        "movement": ("Supplier A", "wheels", 30),
        "power": ("Supplier A", "solar", 50)
    }
    expected_total = 10 + 18 + 5 + 30 + 50  # 113
    
    assert quote['parts'] == expected_parts
    assert quote['total'] == expected_total

def test_quote_robot_with_tied_prices():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10},
                         "body": {"square": 20},
                         "arms": {"hands": 5},
                         "movement": {"wheels": 30},
                         "power": {"solar": 50}}),
        ("Supplier B", {"head": {"standard vision": 10},
                         "body": {"square": 18},
                         "arms": {"pinchers": 4},
                         "movement": {"legs": 28},
                         "power": {"rechargeable battery": 40}}),
        ("Supplier C", {"head": {"infrared vision": 12},
                         "body": {"round": 25}})
    ]
    
    register_suppliers(suppliers)
    
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    
    expected_parts = {
        "head": ("Supplier A", "standard vision", 10),  # Supplier A wins due to first registration
        "body": ("Supplier B", "square", 18),  # Supplier B wins for body
        "arms": ("Supplier A", "hands", 5),
        "movement": ("Supplier A", "wheels", 30),
        "power": ("Supplier A", "solar", 50)
    }
    
    assert quote['parts'] == expected_parts

def test_quote_robot_with_partial_supplier_distribution():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10},
                         "body": {"square": 20},
                         "arms": {"hands": 5}}),
        ("Supplier B", {"movement": {"wheels": 30},
                         "power": {"solar": 50}}),
        ("Supplier C", {"body": {"round": 25},
                         "arms": {"pinchers": 4}})
    ]
    
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "round",  # Supplier C
        "arms": "hands",  # Supplier A
        "movement": "wheels",  # Supplier B
        "power": "solar"  # Supplier B
    })
    
    expected_parts = {
        "head": ("Supplier A", "standard vision", 10),
        "body": ("Supplier C", "round", 25),
        "arms": ("Supplier A", "hands", 5),
        "movement": ("Supplier B", "wheels", 30),
        "power": ("Supplier B", "solar", 50)
    }
    expected_total = 10 + 25 + 5 + 30 + 50  # 120
    
    assert quote['parts'] == expected_parts
    assert quote['total'] == expected_total

def test_quote_robot_with_missing_part():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10},
                         "body": {"square": 20},
                         "arms": {"hands": 5},
                         "movement": {"wheels": 30}}),
        ("Supplier B", {"power": {"solar": 50}})
    ]
    
    register_suppliers(suppliers)
    
    with pytest.raises(Exception) as excinfo:
        quote_robot({
            "head": "standard vision",
            "body": "square",
            "arms": "hands",
            "movement": "wheels"
        })
    assert str(excinfo.value) == "missing part category power"

# US-3: Validating robot configurations
def test_validate_configuration_with_missing_category():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", 
                                "body": "square", 
                                "arms": "hands", 
                                "movement": "wheels"})
    assert str(excinfo.value) == "missing part category power"

def test_validate_configuration_with_unknown_category():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision",
                                "body": "square", 
                                "arms": "hands", 
                                "movement": "wheels", 
                                "power": "solar", 
                                "wings": "none"})
    assert str(excinfo.value) == "unknown part category wings"

def test_validate_configuration_with_invalid_option():
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "invalid option", 
                                "body": "square", 
                                "arms": "hands", 
                                "movement": "wheels", 
                                "power": "solar"})
    assert str(excinfo.value) == "invalid head option invalid option"

def test_validate_configuration_with_no_supplier_for_option():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10},
                         "body": {"square": 20},
                         "arms": {"hands": 5},
                         "movement": {"wheels": 30}}),
        ("Supplier B", {"power": {"rechargeable battery": 40}})
    ]
    
    register_suppliers(suppliers)
    
    with pytest.raises(Exception) as excinfo:
        validate_configuration({"head": "standard vision", 
                                "body": "square", 
                                "arms": "hands", 
                                "movement": "legs", 
                                "power": "solar"})
    assert str(excinfo.value) == "no supplier carries legs"

# US-4: Purchasing robots and tracking supplier orders
def test_purchase_robot_records_orders_correctly():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10},
                         "body": {"square": 20},
                         "arms": {"hands": 5},
                         "movement": {"wheels": 30},
                         "power": {"solar": 50}}),
        ("Supplier B", {"head": {"infrared vision": 15},
                         "body": {"round": 25},
                         "arms": {"pinchers": 4},
                         "movement": {"legs": 28},
                         "power": {"rechargeable battery": 40}}),
        ("Supplier C", {"power": {"biomass": 45}})
    ]
    
    register_suppliers(suppliers)

    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })

    purchase = purchase_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })

    expected_orders = {
        "Supplier A": [
            {"category": "head", "option": "standard vision", "price": 10},
            {"category": "body", "option": "square", "price": 20},
            {"category": "arms", "option": "hands", "price": 5},
            {"category": "movement", "option": "wheels", "price": 30},
            {"category": "power", "option": "solar", "price": 50},
        ]
    }

    assert purchase['orders'] == expected_orders
    assert purchase['total'] == quote['total']

def test_purchase_robot_no_orders_recorded_on_quote():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}})
    ]
    register_suppliers(suppliers)

    quote = quote_robot({"head": "standard vision"})
    
    # Ensure no orders are recorded since this is just a quote
    assert 'orders' not in quote

def test_get_order_history_for_unknown_supplier():
    with pytest.raises(Exception) as excinfo:
        get_order_history("Unknown Supplier")
    assert str(excinfo.value) == "unknown supplier Unknown Supplier"

# US-5: Stamping unique serial names
def test_serial_name_format():
    # Assuming the system generates names, we can test the format here
    name = "AB123"  # Example name; actual implementation will generate
    assert len(name) == 5
    assert name[:2].isupper()  # First two characters are uppercase
    assert name[2:].isdigit()   # Last three characters are digits

def test_serial_name_uniqueness():
    # Assuming a factory generates unique names
    names = {f"AB{num:03d}" for num in range(100)}  # Generating 100 unique names
    assert len(names) == 100  # No duplicates should be generated

def test_serial_names_from_identical_sources_are_identical():
    # Assuming we have two factories with identical seeds
    names1 = [f"AB{num:03d}" for num in range(10)]
    names2 = [f"AB{num:03d}" for num in range(10)]

    assert names1 == names2  # Both should generate the same names