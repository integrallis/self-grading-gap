import pytest
from solution import ParkingLot

def test_configuring_lot_with_negative_motorcycle_spot_count():
    with pytest.raises(Exception) as excinfo:
        ParkingLot({'motorcycle': -1, 'compact': 10, 'large': 10}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert excinfo.value.args == ('motorcycle', -1)  # Check that the exception identifies 'motorcycle' and '-1'

def test_configuring_lot_with_negative_compact_spot_count():
    with pytest.raises(Exception) as excinfo:
        ParkingLot({'motorcycle': 10, 'compact': -1, 'large': 10}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configuring_lot_with_no_spots():
    with pytest.raises(Exception) as excinfo:
        ParkingLot({'motorcycle': 0, 'compact': 0, 'large': 0}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configuring_lot_with_missing_hourly_rate():
    with pytest.raises(Exception) as excinfo:
        ParkingLot({'motorcycle': 10, 'compact': 10, 'large': 10}, {'motorcycle': 1.0, 'bus': 5.0})  # Missing 'car'
    assert excinfo.value.args == ('car',)  # Check that the exception identifies 'car'

def test_configuring_lot_with_non_positive_hourly_rate():
    with pytest.raises(Exception) as excinfo:
        ParkingLot({'motorcycle': 10, 'compact': 10, 'large': 10}, {'motorcycle': 1.0, 'car': -2.0, 'bus': 5.0})
    assert excinfo.value.args == ('car', -2.0)  # Check that the exception identifies 'car' and '-2.0'

def test_motorcycle_parking_in_motorcycle_spot():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    assert ticket['vehicle_id'] == 'M-1'
    assert ticket['spot_type'] == 'motorcycle'

def test_motorcycle_parking_fallback_to_compact_spot():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    ticket = lot.check_in('M-2', 'motorcycle')  # Check in another motorcycle
    assert ticket['vehicle_id'] == 'M-2'
    assert ticket['spot_type'] == 'compact'  # Should fall back to compact

def test_motorcycle_parking_fallback_to_large_spot():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    lot.check_in('M-2', 'motorcycle')  # Check in second motorcycle
    ticket = lot.check_in('M-3', 'motorcycle')  # Check in third motorcycle
    assert ticket['vehicle_id'] == 'M-3'
    assert ticket['spot_type'] == 'large'  # Should fall back to large

def test_car_parking_in_compact_spot():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    ticket = lot.check_in('C-1', 'car')  # Check in car
    assert ticket['vehicle_id'] == 'C-1'
    assert ticket['spot_type'] == 'compact'

def test_car_parking_fallback_to_large_spot():
    lot = ParkingLot({'motorcycle': 1, 'compact': 0, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    ticket = lot.check_in('C-1', 'car')  # Check in car
    assert ticket['vehicle_id'] == 'C-1'
    assert ticket['spot_type'] == 'large'  # Should fall back to large

def test_car_turning_away_when_only_motorcycle_spots_available():
    lot = ParkingLot({'motorcycle': 1, 'compact': 0, 'large': 0}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')
    with pytest.raises(Exception) as excinfo:
        lot.check_in('C-1', 'car')  # Attempt to check in car
    assert str(excinfo.value) == "no available spot for [car]"

def test_bus_parking_in_large_spot():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('C-1', 'car')  # Check in car
    ticket = lot.check_in('B-1', 'bus')  # Check in bus
    assert ticket['vehicle_id'] == 'B-1'
    assert ticket['spot_type'] == 'large'

def test_bus_turning_away_when_no_large_spots_available():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 0}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('C-1', 'car')
    lot.check_in('M-1', 'motorcycle')
    with pytest.raises(Exception) as excinfo:
        lot.check_in('B-1', 'bus')  # Attempt to check in bus
    assert str(excinfo.value) == "no available spot for [bus]"

def test_full_lot_checkin_failure():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')
    lot.check_in('C-1', 'car')
    lot.check_in('B-1', 'bus')
    with pytest.raises(Exception):
        lot.check_in('C-2', 'car')  # Attempt to check in another car
    occupancy = lot.report_occupancy()
    assert occupancy['motorcycle']['available'] == 0
    assert occupancy['compact']['available'] == 0
    assert occupancy['large']['available'] == 0

def test_checking_out_vehicle_that_is_not_parked():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    with pytest.raises(Exception) as excinfo:
        lot.check_out('C-1')  # Attempt to check out car not parked
    assert str(excinfo.value) == "vehicle [C-1] is not parked"

def test_successful_checkout_updates_occupancy():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('C-1', 'car')  # Check in car
    lot.check_out('C-1', ticket['entry_time'])  # Check out car
    assert lot.is_parked('C-1') is False  # Car should no longer be parked

def test_duplicate_check_in_refusal():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    with pytest.raises(Exception) as excinfo:
        lot.check_in('M-1', 'motorcycle')  # Attempt to check in same motorcycle again
    assert str(excinfo.value) == "vehicle [M-1] is already parked"

def test_checkout_and_rearrival():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')  # Check in motorcycle
    lot.check_out('M-1', ticket['entry_time'])  # Check out motorcycle
    ticket2 = lot.check_in('M-1', 'motorcycle')  # Check in motorcycle again
    assert ticket2['vehicle_id'] == 'M-1'  # Should allow re-check in
    assert ticket2['spot_type'] == 'motorcycle'  # Should be the motorcycle spot again

def test_billing_for_zero_length_stay():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    receipt = lot.check_out(ticket['entry_time'])  # Exit at the same time
    assert receipt['billed_hours'] == 1  # Minimum charge is 1 hour
    assert receipt['fee'] == 1.0  # Motorcycle rate is 1.0

def test_billing_for_partial_hours():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    receipt = lot.check_out(ticket['entry_time'] + 5400)  # Check out after 90 minutes
    assert receipt['billed_hours'] == 2  # 90 minutes bills as 2 hours
    assert receipt['fee'] == 2.0  # 2 hours at 1.0 per hour

def test_billing_for_exact_hours():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    receipt = lot.check_out(ticket['entry_time'] + 10800)  # Check out after 3 hours
    assert receipt['billed_hours'] == 3  # Exactly 3 hours
    assert receipt['fee'] == 3.0  # 3 hours at 1.0 per hour

def test_billing_for_ten_minute_stay():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    receipt = lot.check_out(ticket['entry_time'] + 600)  # Check out after 10 minutes
    assert receipt['billed_hours'] == 1  # Minimum charge is 1 hour
    assert receipt['fee'] == 1.0  # Motorcycle rate is 1.0

def test_billing_for_one_second_past_an_hour():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    receipt = lot.check_out(ticket['entry_time'] + 3601)  # Check out after 1 hour and 1 second
    assert receipt['billed_hours'] == 2  # Should round up to 2 hours
    assert receipt['fee'] == 2.0  # 2 hours at 1.0 per hour

def test_exit_time_before_entry_time():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    with pytest.raises(Exception) as excinfo:
        lot.check_out(ticket['entry_time'] - 3600)  # Attempt to check out before entry time
    assert excinfo.value.args == (ticket['entry_time'] - 3600, ticket['entry_time'])  # Check that both times are shown

def test_receipt_contains_all_required_fields():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    receipt = lot.check_out(ticket['entry_time'] + 7200)  # Check out after 2 hours
    assert receipt['vehicle_id'] == 'M-1'
    assert receipt['vehicle_type'] == 'motorcycle'
    assert receipt['spot_type'] == 'motorcycle'
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0
    assert receipt['entry_time'] == ticket['entry_time']  # Ensure entry_time is present
    assert receipt['exit_time'] == ticket['entry_time'] + 7200  # Ensure exit_time is calculated correctly

def test_reporting_occupancy():
    lot = ParkingLot({'motorcycle': 2, 'compact': 2, 'large': 2}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in('M-1', 'motorcycle')
    lot.check_in('C-1', 'car')
    occupancy = lot.report_occupancy()
    assert occupancy['motorcycle']['capacity'] == 2
    assert occupancy['motorcycle']['occupied'] == 1
    assert occupancy['motorcycle']['available'] == 1
    assert occupancy['compact']['capacity'] == 2
    assert occupancy['compact']['occupied'] == 1
    assert occupancy['compact']['available'] == 1
    assert occupancy['large']['capacity'] == 2
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 2

def test_availability_increases_after_checkout():
    lot = ParkingLot({'motorcycle': 1, 'compact': 1, 'large': 1}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in('M-1', 'motorcycle')
    lot.check_out('M-1', ticket['entry_time'])
    occupancy = lot.report_occupancy()
    assert occupancy['motorcycle']['available'] == 1  # Should increase after checkout

def test_multiple_vehicles_of_same_type_checkout():
    lot = ParkingLot({'motorcycle': 2, 'compact': 2, 'large': 2}, {'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket1 = lot.check_in('M-1', 'motorcycle')
    ticket2 = lot.check_in('M-2', 'motorcycle')  # Two motorcycles
    lot.check_out('M-1', ticket1['entry_time'])
    assert lot.is_parked('M-1') is False  # M-1 should no longer be parked
    assert lot.is_parked('M-2') is True   # M-2 should still be parked
    lot.check_out('M-2', ticket2['entry_time'])
    assert lot.is_parked('M-2') is False  # Now M-2 should also be checked out