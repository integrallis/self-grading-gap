import pytest
from solution import register_suppliers, quote_robot, validate_configuration, purchase_robot, RandomnessSource

# US-1: Registering a healthy supplier pool
def test_register_suppliers_rejects_fewer_than_three():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        register_suppliers(['SupplierA', 'SupplierB'])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 2"

def test_register_suppliers_rejects_fewer_than_three_1():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        register_suppliers([])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 0"

def test_register_suppliers_rejects_fewer_than_three_2():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        register_suppliers(['SupplierA'])
    assert str(excinfo.value) == "at least 3 suppliers are required, got 1"

def test_register_suppliers_rejects_duplicate_supplier_names():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        register_suppliers(['SupplierA', 'SupplierB', 'SupplierA'])
    assert str(excinfo.value) == "duplicate supplier name SupplierA"

# US-2: Quoting a robot at the lowest cost
def test_quote_robot_sources_parts_lowest_cost():
    suppliers = {
        'SupplierA': {'head': {'standard vision': 50}, 'body': {'square': 60}, 'arms': {'hands': 30}, 'movement': {'wheels': 40}, 'power': {'solar': 20}},
        'SupplierB': {'head': {'standard vision': 55}, 'body': {'square': 65}, 'arms': {'hands': 35}, 'movement': {'wheels': 40}, 'power': {'solar': 25}},
        'SupplierC': {'head': {'standard vision': 50}, 'body': {'round': 70}, 'arms': {'hands': 32}, 'movement': {'legs': 45}, 'power': {'solar': 20}},
    }
    total_cost = 50 + 60 + 30 + 40 + 20  # 200
    quote = quote_robot(suppliers, 'standard vision', 'square', 'hands', 'wheels', 'solar')
    assert quote['total'] == total_cost
    assert len(quote['parts']) == 5  # Ensure there are 5 parts in the quote
    assert quote['parts'][0]['category'] == 'head'
    assert quote['parts'][0]['supplier'] == 'SupplierA'
    assert quote['parts'][0]['price'] == 50
    assert quote['parts'][1]['category'] == 'body'
    assert quote['parts'][1]['supplier'] == 'SupplierA'
    assert quote['parts'][1]['price'] == 60
    assert quote['parts'][2]['category'] == 'arms'
    assert quote['parts'][2]['supplier'] == 'SupplierA'
    assert quote['parts'][2]['price'] == 30
    assert quote['parts'][3]['category'] == 'movement'
    assert quote['parts'][3]['supplier'] == 'SupplierA'
    assert quote['parts'][3]['price'] == 40
    assert quote['parts'][4]['category'] == 'power'
    assert quote['parts'][4]['supplier'] == 'SupplierA'
    assert quote['parts'][4]['price'] == 20

def test_quote_robot_handles_ties():
    suppliers = {
        'SupplierA': {'head': {'standard vision': 50}},
        'SupplierB': {'head': {'standard vision': 50}},
        'SupplierC': {'head': {'standard vision': 55}},
        'SupplierD': {'body': {'square': 60}},
    }
    quote = quote_robot(suppliers, 'standard vision', 'square', 'hands', 'wheels', 'solar')
    assert quote['parts'][0]['supplier'] == 'SupplierA'  # First registered supplier wins

def test_quote_robot_handles_unavailable_parts():
    suppliers = {
        'SupplierA': {'head': {'standard vision': 50}, 'body': {'square': 60}},
        'SupplierB': {'arms': {'hands': 30}, 'movement': {'wheels': 40}},
        'SupplierC': {'power': {'solar': 20}},
    }
    with pytest.raises(Exception) as excinfo:  # Assuming a dedicated part-unavailability error
        quote_robot(suppliers, 'standard vision', 'square', 'hands', 'wheels', 'biomass')
    assert str(excinfo.value) == "no supplier carries biomass"

def test_quote_robot_sources_multiple_suppliers():
    suppliers = {
        'SupplierA': {'head': {'standard vision': 50}, 'body': {'square': 60}},
        'SupplierB': {'arms': {'hands': 30}},
        'SupplierC': {'movement': {'wheels': 40}, 'power': {'solar': 20}},
    }
    total_cost = 50 + 60 + 30 + 40 + 20  # 200
    quote = quote_robot(suppliers, 'standard vision', 'square', 'hands', 'wheels', 'solar')
    assert quote['total'] == total_cost

# US-3: Validating robot configurations
def test_validate_configuration_rejects_missing_category():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        validate_configuration({'head': 'standard vision', 'body': 'square', 'arms': 'hands', 'movement': 'wheels'})
    assert str(excinfo.value) == "missing part category power"

def test_validate_configuration_rejects_unknown_category():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        validate_configuration({'head': 'standard vision', 'body': 'square', 'arms': 'hands', 'movement': 'wheels', 'power': 'solar', 'extra': 'value'})
    assert str(excinfo.value) == "unknown part category extra"

def test_validate_configuration_rejects_invalid_option():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        validate_configuration({'head': 'invalid option', 'body': 'square', 'arms': 'hands', 'movement': 'wheels', 'power': 'solar'})
    assert str(excinfo.value) == "invalid head option invalid option"

def test_validate_configuration_accepts_valid_options():
    valid_options = {
        'head': ['standard vision', 'infrared vision', 'night vision'],
        'body': ['square', 'round', 'triangular', 'rectangular'],
        'arms': ['hands', 'pinchers', 'boxing gloves'],
        'movement': ['wheels', 'legs', 'tracks'],
        'power': ['solar', 'rechargeable battery', 'biomass'],
    }
    for category, options in valid_options.items():
        for option in options:
            config = {category: option, 'head': 'standard vision', 'body': 'square', 'arms': 'hands', 'movement': 'wheels', 'power': 'solar'}
            validate_configuration(config)

# US-4: Purchasing robots and tracking supplier orders
def test_purchase_robot_records_orders():
    suppliers = {
        'SupplierA': {'head': {'standard vision': 50}, 'body': {'square': 60}, 'arms': {'hands': 30}, 'movement': {'wheels': 40}, 'power': {'solar': 20}},
        'SupplierB': {'head': {'standard vision': 55}, 'body': {'round': 70}, 'arms': {'hands': 32}, 'movement': {'legs': 45}, 'power': {'solar': 25}},
        'SupplierC': {'power': {'biomass': 30}},
    }
    quote = quote_robot(suppliers, 'standard vision', 'square', 'hands', 'wheels', 'solar')
    purchase = purchase_robot(quote)
    assert purchase['total'] == quote['total']
    assert len(purchase['orders']) == 5  # Ensure orders are recorded
    assert purchase['orders'][0]['supplier'] == 'SupplierA'
    assert purchase['orders'][0]['category'] == 'head'
    assert purchase['orders'][0]['option'] == 'standard vision'
    assert purchase['orders'][0]['price'] == 50

def test_purchase_robot_records_no_orders_on_quote():
    suppliers = {
        'SupplierA': {'head': {'standard vision': 50}},
        'SupplierB': {'body': {'square': 60}},
        'SupplierC': {'arms': {'hands': 30}},
    }
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        quote_robot(suppliers, 'standard vision', 'square', 'hands', 'wheels', 'solar')

def test_purchase_robot_rejects_unknown_supplier():
    with pytest.raises(Exception) as excinfo:  # Assuming a generic exception
        purchase_robot([], 'UnknownSupplier')
    assert str(excinfo.value) == "unknown supplier UnknownSupplier"

# US-5: Stamping unique serial names
def test_robot_serial_name_format():
    randomness_source = RandomnessSource(seed=1)
    purchased_robot = purchase_robot([], randomness_source)
    name = purchased_robot['name']
    assert len(name) == 5  # Length must be 5
    assert name[:2].isupper()  # First two characters are uppercase
    assert name[2:].isdigit()  # Last three characters are digits

def test_robot_serial_names_are_unique():
    randomness_source = RandomnessSource(seed=1)
    names = set()
    for _ in range(10):
        purchased_robot = purchase_robot([], randomness_source)
        names.add(purchased_robot['name'])
    assert len(names) == 10  # All names must be unique

def test_robot_serial_names_are_reproducible():
    randomness_source1 = RandomnessSource(seed=1)
    randomness_source2 = RandomnessSource(seed=1)
    purchase1 = purchase_robot([], randomness_source1)
    purchase2 = purchase_robot([], randomness_source2)
    assert purchase1['name'] == purchase2['name']  # Same seed should produce same name