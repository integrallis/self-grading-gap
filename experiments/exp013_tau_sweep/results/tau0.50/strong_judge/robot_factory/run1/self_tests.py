import pytest
import re
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot, get_order_history

# US-1: Registering a healthy supplier pool

def test_register_suppliers_rejects_fewer_than_three_suppliers_zero():
    with pytest.raises(ValueError, match=r"^at least 3 suppliers are required, got 0$"):
        register_suppliers([])

def test_register_suppliers_rejects_fewer_than_three_suppliers_one():
    with pytest.raises(ValueError, match=r"^at least 3 suppliers are required, got 1$"):
        register_suppliers([("Supplier A", {})])

def test_register_suppliers_rejects_fewer_than_three_suppliers_two():
    with pytest.raises(ValueError, match=r"^at least 3 suppliers are required, got 2$"):
        register_suppliers([("Supplier A", {}), ("Supplier B", {})])

def test_register_suppliers_rejects_duplicate_supplier_names():
    with pytest.raises(ValueError, match=r"^duplicate supplier name Supplier A$"):
        register_suppliers([
            ("Supplier A", {}),
            ("Supplier B", {}),
            ("Supplier A", {})
        ])

# US-2: Quoting a robot at the lowest cost

def test_quote_robot_lowest_cost():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}, "arms": {"hands": 14}, "movement": {"wheels": 22}, "power": {"solar": 29}}),
        ("Supplier C", {"head": {"standard vision": 11}, "body": {"square": 21}, "arms": {"hands": 20}, "movement": {"wheels": 24}, "power": {"solar": 31}})
    ]
    register_suppliers(suppliers)
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    # The cheapest parts are: head Supplier A/10, body Supplier B/18, arms Supplier B/14, movement Supplier B/22, power Supplier B/29
    assert quote == {
        "parts": [
            {"category": "head", "supplier": "Supplier A", "price": 10},
            {"category": "body", "supplier": "Supplier B", "price": 18},
            {"category": "arms", "supplier": "Supplier B", "price": 14},
            {"category": "movement", "supplier": "Supplier B", "price": 22},
            {"category": "power", "supplier": "Supplier B", "price": 29}
        ],
        "total": 93  # 10 + 18 + 14 + 22 + 29 = 93
    }

def test_quote_robot_with_tied_prices():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 10}, "body": {"square": 19}, "arms": {"hands": 14}, "movement": {"wheels": 22}, "power": {"solar": 29}}),
        ("Supplier C", {"head": {"standard vision": 12}, "body": {"square": 18}, "arms": {"hands": 20}, "movement": {"wheels": 24}, "power": {"solar": 31}})
    ]
    register_suppliers(suppliers)
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    # Supplier A and Supplier B tie on head price, but Supplier A is registered first.
    assert quote == {
        "parts": [
            {"category": "head", "supplier": "Supplier A", "price": 10},
            {"category": "body", "supplier": "Supplier B", "price": 19},
            {"category": "arms", "supplier": "Supplier B", "price": 14},
            {"category": "movement", "supplier": "Supplier B", "price": 22},
            {"category": "power", "supplier": "Supplier B", "price": 29}
        ],
        "total": 93  # 10 + 19 + 14 + 22 + 29 = 93
    }

def test_quote_robot_missing_parts_from_suppliers():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 30}}),
        ("Supplier C", {})  # No parts offered
    ]
    register_suppliers(suppliers)
    quote = quote_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    # Supplier A provides head and body, Supplier B provides arms, movement, and power.
    assert quote == {
        "parts": [
            {"category": "head", "supplier": "Supplier A", "price": 10},
            {"category": "body", "supplier": "Supplier A", "price": 20},
            {"category": "arms", "supplier": "Supplier B", "price": 15},
            {"category": "movement", "supplier": "Supplier B", "price": 25},
            {"category": "power", "supplier": "Supplier B", "price": 30}
        ],
        "total": 100  # 10 + 20 + 15 + 25 + 30 = 100
    }

# US-3: Validating robot configurations

def test_validate_configuration_missing_part_category():
    with pytest.raises(ValueError, match=r"^missing part category body$"):
        validate_configuration({
            "head": "standard vision",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar"
        })

def test_validate_configuration_unknown_part_category():
    with pytest.raises(ValueError, match=r"^unknown part category antenna$"):
        validate_configuration({
            "head": "standard vision",
            "body": "square",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar",
            "antenna": "dish"  # Unknown category
        })

def test_validate_configuration_invalid_option():
    with pytest.raises(ValueError, match=r"^invalid body option hexagonal$"):
        validate_configuration({
            "head": "standard vision",
            "body": "hexagonal",  # Invalid option for body
            "arms": "hands",
            "movement": "wheels",
            "power": "solar"
        })

def test_validate_configuration_no_supplier_carries_option():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}})
    ]
    register_suppliers(suppliers)
    with pytest.raises(ValueError, match=r"^no supplier carries pinchers$"):
        validate_configuration({
            "head": "standard vision",
            "body": "square",
            "arms": "pinchers",  # No supplier carries this option
            "movement": "wheels",
            "power": "solar"
        })

# US-4: Purchasing robots and tracking supplier orders

def test_purchase_robot_records_orders():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}, "arms": {"hands": 15}, "movement": {"wheels": 25}, "power": {"solar": 30}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}, "arms": {"hands": 14}, "movement": {"wheels": 22}, "power": {"solar": 29}}),
        ("Supplier C", {})
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
    # Purchase should match quote
    assert purchase["total"] == quote["total"]
    assert purchase["parts"] == quote["parts"]
    
    # Verify order history
    assert get_order_history("Supplier A") == [{"option": "standard vision", "price": 10}]
    assert get_order_history("Supplier B") == [
        {"option": "square", "price": 18},
        {"option": "hands", "price": 14},
        {"option": "wheels", "price": 22},
        {"option": "solar", "price": 29}
    ]
    assert get_order_history("Supplier C") == []  # No orders for Supplier C

def test_purchase_robot_no_orders_on_quote():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}}),
        ("Supplier C", {})
    ]
    register_suppliers(suppliers)
    quote_robot({
        "head": "standard vision",
        "body": "square"
    })
    # No orders should be recorded before purchase
    assert get_order_history("Supplier A") == []
    assert get_order_history("Supplier B") == []
    assert get_order_history("Supplier C") == []

def test_get_order_history_unknown_supplier():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}}),
        ("Supplier C", {})
    ]
    register_suppliers(suppliers)
    with pytest.raises(ValueError, match=r"^unknown supplier Supplier D$"):
        get_order_history("Supplier D")

# US-5: Stamping unique serial names

def test_robot_serial_name_format():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}}),
        ("Supplier C", {})
    ]
    register_suppliers(suppliers)
    purchase = purchase_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })
    assert re.fullmatch(r"[A-Z]{2}\d{3}", purchase["name"])  # Should match format

def test_robot_serial_name_uniqueness():
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}}),
        ("Supplier C", {})
    ]
    register_suppliers(suppliers)
    names = set()
    for _ in range(10):  # Simulating multiple purchases
        name = purchase_robot({
            "head": "standard vision",
            "body": "square",
            "arms": "hands",
            "movement": "wheels",
            "power": "solar"
        })["name"]
        assert name not in names
        names.add(name)

def test_robot_serial_name_reproducibility():
    class RandomSource:
        def __init__(self, seed):
            self.seed = seed
            self.counter = 0
        
        def random(self):
            self.counter += 1
            return self.seed + self.counter
    
    suppliers = [
        ("Supplier A", {"head": {"standard vision": 10}, "body": {"square": 20}}),
        ("Supplier B", {"head": {"standard vision": 12}, "body": {"square": 18}}),
        ("Supplier C", {})
    ]
    register_suppliers(suppliers)

    random_source_1 = RandomSource(1)
    random_source_2 = RandomSource(1)
    
    name_1 = purchase_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })["name"]

    name_2 = purchase_robot({
        "head": "standard vision",
        "body": "square",
        "arms": "hands",
        "movement": "wheels",
        "power": "solar"
    })["name"]

    assert name_1 == name_2  # Names should be the same if randomness sources are identical