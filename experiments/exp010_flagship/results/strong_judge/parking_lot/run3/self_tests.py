import pytest
from solution import ParkingLot

def test_configuring_lot_with_valid_configuration():
    lot = ParkingLot(
        spots={
            'motorcycle': 5,
            'compact': 10,
            'large': 15
        },
        rates={
            'motorcycle': 1.0,
            'car': 2.0,
            'bus': 5.0
        }
    )
    assert lot is not None  # Successfully created a parking lot

def test_configuring_lot_with_negative_motorcycle_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': -1,  # Invalid count
                'compact': 10,
                'large': 15
            },
            rates={
                'motorcycle': 1.0,
                'car': 2.0,
                'bus': 5.0
            }
        )
    assert str(excinfo.value) == "spot count for [motorcycle] must be non-negative, got [-1]"

def test_configuring_lot_with_negative_compact_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': -1,  # Invalid count
                'large': 15
            },
            rates={
                'motorcycle': 1.0,
                'car': 2.0,
                'bus': 5.0
            }
        )
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configuring_lot_with_negative_large_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': 10,
                'large': -1  # Invalid count
            },
            rates={
                'motorcycle': 1.0,
                'car': 2.0,
                'bus': 5.0
            }
        )
    assert str(excinfo.value) == "spot count for [large] must be non-negative, got [-1]"

def test_configuring_lot_with_no_spots():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 0,
                'compact': 0,
                'large': 0
            },
            rates={
                'motorcycle': 1.0,
                'car': 2.0,
                'bus': 5.0
            }
        )
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configuring_lot_with_missing_hourly_rate_motorcycle():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': 10,
                'large': 15
            },
            rates={
                'car': 2.0,
                'bus': 5.0
                # Missing rate for motorcycle
            }
        )
    assert "missing hourly rate for [motorcycle]" in str(excinfo.value)

def test_configuring_lot_with_missing_hourly_rate_car():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': 10,
                'large': 15
            },
            rates={
                'motorcycle': 1.0,
                'bus': 5.0
                # Missing rate for car
            }
        )
    assert "missing hourly rate for [car]" in str(excinfo.value)

def test_configuring_lot_with_missing_hourly_rate_bus():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': 10,
                'large': 15
            },
            rates={
                'motorcycle': 1.0,
                'car': 2.0,
                # Missing rate for bus
            }
        )
    assert "missing hourly rate for [bus]" in str(excinfo.value)

def test_configuring_lot_with_non_positive_hourly_rate_zero():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': 10,
                'large': 15
            },
            rates={
                'motorcycle': 1.0,
                'car': 0.0,  # Invalid rate
                'bus': 5.0
            }
        )
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_configuring_lot_with_non_positive_hourly_rate_negative():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(
            spots={
                'motorcycle': 5,
                'compact': 10,
                'large': 15
            },
            rates={
                'motorcycle': 1.0,
                'car': -2.0,  # Invalid rate
                'bus': 5.0
            }
        )
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [-2.0]"

def test_motorcycle_parks_in_motorcycle_spot():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('M-1', 'motorcycle', 1000.0)
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'motorcycle'

def test_motorcycle_parks_in_compact_spot_when_motorcycle_spot_full():
    lot = ParkingLot(
        spots={'motorcycle': 0, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('M-1', 'motorcycle', 1000.0)
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'compact'

def test_motorcycle_parks_in_large_spot_when_compact_spot_full():
    lot = ParkingLot(
        spots={'motorcycle': 0, 'compact': 0, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('M-1', 'motorcycle', 1000.0)
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'large'

def test_car_parks_in_compact_spot():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('C-1', 'car', 1000.0)
    assert ticket['vehicle_id'] == 'C-1'
    assert ticket['spot_type'] == 'compact'

def test_car_turns_away_when_no_compact_spots():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 0, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('C-1', 'car', 1000.0)  # Fill the large spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in('C-2', 'car', 1001.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_bus_parks_in_large_spot():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('B-1', 'bus', 1000.0)
    assert ticket['vehicle_id'] == 'B-1'
    assert ticket['spot_type'] == 'large'

def test_bus_turns_away_when_no_large_spots():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 0},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    with pytest.raises(ValueError) as excinfo:
        lot.check_in('B-1', 'bus', 1000.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_checking_in_full_lot_reports_full():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('M-1', 'motorcycle', 1000.0)
    lot.check_in('C-1', 'car', 1001.0)
    lot.check_in('B-1', 'bus', 1002.0)  # Fill the large spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in('C-2', 'car', 1003.0)
    # Test that full status is reflected, but no exact message is asserted
    assert str(excinfo.value) == "no available spot for [car]"

def test_checking_out_frees_spot():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('M-1', 'motorcycle', 1000.0)
    lot.check_out('M-1', 1100.0)  # 1 hour stay
    assert lot.is_parked('M-1') is False
    # Check that the spot can now be reused
    ticket = lot.check_in('M-2', 'motorcycle', 1101.0)
    assert ticket['vehicle_id'] == 'M-2'
    assert ticket['spot_type'] == 'motorcycle'

def test_checking_out_a_vehicle_not_parked():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    with pytest.raises(ValueError) as excinfo:
        lot.check_out('ghost', 1100.0)
    assert "vehicle [ghost] is not parked" in str(excinfo.value)

def test_billing_for_one_hour_stay():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('M-1', 'motorcycle', 1000.0)
    receipt = lot.check_out('M-1', 1060.0)  # 1 hour stay
    assert receipt['billed_hours'] == 1  # 1 hour
    assert receipt['fee'] == 1.0  # 1 hour * 1.0 rate

def test_billing_for_ten_minute_stay():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('M-1', 'motorcycle', 1000.0)
    receipt = lot.check_out('M-1', 1010.0)  # 10 minute stay
    assert receipt['billed_hours'] == 1  # Rounded up
    assert receipt['fee'] == 1.0  # 1 hour * 1.0 rate

def test_billing_for_partial_hours_rounding_up():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('C-1', 'car', 1000.0)
    receipt = lot.check_out('C-1', 1160.0)  # 2 hours 40 minutes
    assert receipt['billed_hours'] == 3  # Rounded up
    assert receipt['fee'] == 6.0  # 3 hours * 2.0 rate

def test_billing_for_exact_hours():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('C-1', 'car', 1000.0)
    receipt = lot.check_out('C-1', 1200.0)  # 2 hours stay
    assert receipt['billed_hours'] == 2  # Exactly 2 hours
    assert receipt['fee'] == 4.0  # 2 hours * 2.0 rate

def test_exit_time_before_entry_time():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('C-1', 'car', 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out('C-1', 900.0)  # Invalid exit time
    assert "exit_time [900.0] is before entry_time [1000.0]" in str(excinfo.value)

def test_receipt_contains_correct_information():
    lot = ParkingLot(
        spots={'motorcycle': 1, 'compact': 1, 'large': 1},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    ticket = lot.check_in('C-1', 'car', 1000.0)
    receipt = lot.check_out('C-1', 1200.0)  # 2 hours stay
    assert receipt['vehicle_id'] == 'C-1'
    assert receipt['vehicle_type'] == 'car'
    assert receipt['spot_type'] == 'compact'
    assert receipt['entry_time'] == 1000.0
    assert receipt['exit_time'] == 1200.0
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 4.0  # 2 hours * 2.0 rate

def test_reporting_occupancy():
    lot = ParkingLot(
        spots={'motorcycle': 2, 'compact': 2, 'large': 2},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('M-1', 'motorcycle', 1000.0)
    lot.check_in('C-1', 'car', 1001.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['total'] == 2
    assert occupancy['motorcycle']['occupied'] == 1
    assert occupancy['compact']['total'] == 2
    assert occupancy['compact']['occupied'] == 1
    assert occupancy['large']['total'] == 2
    assert occupancy['large']['occupied'] == 0

def test_available_count_decreases_on_check_in():
    lot = ParkingLot(
        spots={'motorcycle': 2, 'compact': 2, 'large': 2},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('M-1', 'motorcycle', 1000.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['available'] == 1

def test_available_count_increases_on_check_out():
    lot = ParkingLot(
        spots={'motorcycle': 2, 'compact': 2, 'large': 2},
        rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0}
    )
    lot.check_in('M-1', 'motorcycle', 1000.0)
    lot.check_out('M-1', 1100.0)  # 1 hour stay
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['available'] == 2