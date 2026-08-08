# test_parking_lot.py

import pytest
from solution import ParkingLot

def test_configure_parking_lot_with_valid_configuration():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})

def test_configure_parking_lot_with_negative_spot_count():
    lot = ParkingLot()
    with pytest.raises(Exception) as exc:
        lot.configure(spots={'motorcycle': 1, 'compact': -1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert "spot count for [compact] must be non-negative, got [-1]" in str(exc.value)

def test_configure_parking_lot_with_no_spots():
    lot = ParkingLot()
    with pytest.raises(Exception) as exc:
        lot.configure(spots={'motorcycle': 0, 'compact': 0, 'large': 0}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert "parking lot must have at least one spot" in str(exc.value)

def test_configure_parking_lot_with_missing_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(Exception) as exc:
        lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0})
    assert "missing hourly rate for [bus]" in str(exc.value)

def test_configure_parking_lot_with_non_positive_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(Exception) as exc:
        lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 0.0, 'bus': 5.0})
    assert "hourly rate for [car] must be positive, got [0.0]" in str(exc.value)

def test_configure_parking_lot_with_negative_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(Exception) as exc:
        lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': -1.0, 'car': 2.0, 'bus': 5.0})
    assert "hourly rate for [motorcycle] must be positive, got [-1.0]" in str(exc.value)

def test_motorcycle_parks_in_motorcycle_spot():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 1000, 'motorcycle')
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'motorcycle'
    assert ticket['vehicle_type'] == 'motorcycle'

def test_motorcycle_parks_in_compact_spot_when_no_motorcycle_spots():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 0, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 1000, 'motorcycle')
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'compact'
    assert ticket['vehicle_type'] == 'motorcycle'

def test_motorcycle_parks_in_large_spot_when_no_compact_spots():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 0, 'compact': 0, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 1000, 'motorcycle')
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'large'
    assert ticket['vehicle_type'] == 'motorcycle'

def test_car_parks_in_compact_spot():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('C-1', 1000, 'car')
    assert ticket['vehicle_id'] == 'C-1'
    assert ticket['spot_type'] == 'compact'
    assert ticket['vehicle_type'] == 'car'

def test_car_parks_in_large_spot_when_no_compact_spots():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 0, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('C-1', 1000, 'car')
    assert ticket['vehicle_id'] == 'C-1'
    assert ticket['spot_type'] == 'large'
    assert ticket['vehicle_type'] == 'car'

def test_car_turned_away_when_no_compact_spots():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 0, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('B-1', 1000, 'bus')  # Park the bus first
    with pytest.raises(Exception) as exc:
        lot.check_in('C-1', 1000, 'car')
    assert "no available spot for [car]" in str(exc.value)

def test_bus_parks_in_large_spot():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('B-1', 1000, 'bus')
    assert ticket['vehicle_id'] == 'B-1'
    assert ticket['spot_type'] == 'large'
    assert ticket['vehicle_type'] == 'bus'

def test_bus_turned_away_when_no_large_spots():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 0}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    with pytest.raises(Exception) as exc:
        lot.check_in('B-1', 1000, 'bus')
    assert "no available spot for [bus]" in str(exc.value)

def test_checkout_frees_spot():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    lot.check_out('M-1', exit_time=1100)  # 1 hour stay
    assert lot.report_occupancy()['motorcycle']['occupied'] == 0

def test_checkout_not_parking_vehicle():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    with pytest.raises(Exception) as exc:
        lot.check_out('ghost', exit_time=1100)
    assert "vehicle [ghost] is not parked" in str(exc.value)

def test_duplicate_check_in():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    with pytest.raises(Exception) as exc:
        lot.check_in('M-1', 1100, 'motorcycle')
    assert "vehicle [M-1] is already parked" in str(exc.value)

def test_billing_for_zero_length_stay():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    receipt = lot.check_out('M-1', exit_time=1000)  # 0 hours
    assert receipt['billed_hours'] == 1  # Minimum charge is 1 hour
    assert receipt['fee'] == 1.0  # 1 hour at 1.0 per hour

def test_billing_for_ten_minute_stay():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    receipt = lot.check_out('M-1', exit_time=1010)  # 10 minutes
    assert receipt['billed_hours'] == 1  # Minimum charge is 1 hour
    assert receipt['fee'] == 1.0  # 1 hour at 1.0 per hour

def test_billing_for_partial_hour():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    receipt = lot.check_out('M-1', exit_time=1180)  # 1 hour 20 minutes
    assert receipt['billed_hours'] == 2  # Rounds up to 2 hours
    assert receipt['fee'] == 2.0  # 2 hours at 1.0 per hour

def test_billing_for_exact_hours():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    receipt = lot.check_out('M-1', exit_time=1300)  # Exactly 3 hours
    assert receipt['billed_hours'] == 3  # Exactly 3 hours
    assert receipt['fee'] == 3.0  # 3 hours at 1.0 per hour

def test_exit_time_before_entry_time():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    with pytest.raises(Exception) as exc:
        lot.check_out('M-1', exit_time=999)
    assert "exit_time [999] is before entry_time [1000]" in str(exc.value)

def test_report_occupancy():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    occupancy = lot.report_occupancy()
    assert occupancy['motorcycle']['capacity'] == 1
    assert occupancy['motorcycle']['occupied'] == 1
    assert occupancy['motorcycle']['available'] == 0
    assert occupancy['compact']['capacity'] == 1
    assert occupancy['compact']['occupied'] == 0
    assert occupancy['compact']['available'] == 1
    assert occupancy['large']['capacity'] == 1
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 1

def test_checkout_increases_available_count():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    lot.check_out('M-1', exit_time=1100)
    occupancy = lot.report_occupancy()
    assert occupancy['motorcycle']['available'] == 1

def test_multiple_same_type_vehicles_check_out_independently():
    lot = ParkingLot()
    lot.configure(spots={'motorcycle': 2, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 1000, 'motorcycle')
    lot.check_in('M-2', 1100, 'motorcycle')
    
    receipt1 = lot.check_out('M-1', exit_time=1200)  # 2 hours for M-1
    assert receipt1['billed_hours'] == 2
    assert receipt1['fee'] == 2.0  # 2 hours at 1.0 per hour

    receipt2 = lot.check_out('M-2', exit_time=1300)  # 1 hour for M-2
    assert receipt2['billed_hours'] == 1
    assert receipt2['fee'] == 1.0  # 1 hour at 1.0 per hour