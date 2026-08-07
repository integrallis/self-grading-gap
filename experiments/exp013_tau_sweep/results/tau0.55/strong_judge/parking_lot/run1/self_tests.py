# your complete test file
import pytest
from solution import ParkingLot

# US-1: Configuring the lot
def test_negative_motorcycle_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": -1, "compact": 0, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "spot count for [motorcycle] must be non-negative, got [-1]"

def test_negative_compact_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": 1, "compact": -1, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_negative_large_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": 1, "compact": 0, "large": -1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "spot count for [large] must be non-negative, got [-1]"

def test_no_spots():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": 0, "compact": 0, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_missing_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0})
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_non_positive_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": -2.0, "bus": 5.0})
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [-2.0]"

def test_zero_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 0.0, "bus": 5.0})
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

# US-2: Assigning spots on arrival
def test_motorcycle_parking():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", "motorcycle", 1.0)
    assert ticket['vehicle_id'] == "M-1"
    assert ticket['spot_type'] == "motorcycle"

def test_motorcycle_falls_back_to_compact():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", "motorcycle", 1.0)
    ticket = lot.check_in("M-2", "motorcycle", 1.0)  # Second motorcycle
    assert ticket['vehicle_id'] == "M-2"
    assert ticket['spot_type'] == "compact"

def test_motorcycle_falls_back_to_large():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 0, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", "motorcycle", 1.0)
    ticket = lot.check_in("M-2", "motorcycle", 1.0)  # Second motorcycle
    assert ticket['vehicle_id'] == "M-2"
    assert ticket['spot_type'] == "large"

def test_car_parking():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", "motorcycle", 1.0)
    ticket = lot.check_in("C-1", "car", 1.0)
    assert ticket['vehicle_id'] == "C-1"
    assert ticket['spot_type'] == "compact"

def test_car_falls_back_to_large():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 0, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", "motorcycle", 1.0)
    ticket = lot.check_in("C-1", "car", 1.0)  # No compact, should go to large
    assert ticket['vehicle_id'] == "C-1"
    assert ticket['spot_type'] == "large"

def test_no_spot_for_car():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 0, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", "motorcycle", 1.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_no_spot_for_bus():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", "motorcycle", 1.0)
    lot.check_in("C-1", "car", 1.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("B-1", "bus", 1.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_full_lot():
    lot = ParkingLot(spots={"motorcycle": 0, "compact": 0, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("B-1", "bus", 1.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("B-2", "bus", 1.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_already_parked_vehicle():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1.0)
    assert str(excinfo.value) == "vehicle [C-1] is already parked"

def test_successfully_checked_in_vehicle_is_parked():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    assert lot.is_parked("C-1") is True

# US-3: Checking out
def test_checkout_success():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 2.0)  # Assuming entry time was at 1.0
    assert lot.is_parked("C-1") is False
    assert receipt['vehicle_id'] == 'C-1'
    assert receipt['vehicle_type'] == 'car'
    assert receipt['spot_type'] == 'compact'
    assert receipt['entry_time'] == 1.0
    assert receipt['exit_time'] == 2.0
    assert receipt['billed_hours'] == 1
    assert receipt['fee'] == 2.0  # 1 hour at $2.0

def test_checkout_not_parked():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("ghost", 2.0)
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_independent_checkouts():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 2, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    lot.check_in("C-2", "car", 1.0)
    lot.check_out("C-1", 2.0)  # Assuming entry time was at 1.0
    assert lot.is_parked("C-1") is False
    assert lot.is_parked("C-2") is True

def test_checkout_frees_spot():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    lot.check_out("C-1", 2.0)  # Assuming entry time was at 1.0
    ticket = lot.check_in("C-2", "car", 1.0)  # Should succeed now
    assert ticket['vehicle_id'] == "C-2"
    assert ticket['spot_type'] == "compact"

# US-4: Billing the stay
def test_billing_minimum_charge():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 1.0)  # 0 hours
    assert receipt['fee'] == 2.0  # 1 hour charge

def test_billing_ten_minutes():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 1.1667)  # 10 minutes (~0.1667 hours)
    assert receipt['fee'] == 2.0  # 1 hour charge

def test_billing_partial_hours():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 2.5)  # 1.5 hours
    assert receipt['fee'] == 4.0  # 2 hours charge

def test_billing_exact_hours():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 4.0)  # 3 hours
    assert receipt['fee'] == 6.0  # 3 hours charge

def test_billing_one_second_past_whole_hour():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 2.0001)  # 1 hour and 1 second
    assert receipt['fee'] == 4.0  # 2 hours charge (1 hour + 1 second)

def test_billing_exit_before_entry():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 2.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("C-1", 1.0)  # Exit before entry
    assert str(excinfo.value) == "exit_time [1.0] is before entry_time [2.0]"

def test_checkout_receipt():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    receipt = lot.check_out("C-1", 4.0)  # 3 hours
    assert receipt['vehicle_id'] == 'C-1'
    assert receipt['vehicle_type'] == 'car'
    assert receipt['spot_type'] == 'compact'
    assert receipt['entry_time'] == 1.0
    assert receipt['exit_time'] == 4.0
    assert receipt['billed_hours'] == 3
    assert receipt['fee'] == 6.0

# US-5: Reporting occupancy
def test_occupancy_report():
    lot = ParkingLot(spots={"motorcycle": 2, "compact": 2, "large": 2}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['capacity'] == 2
    assert occupancy['motorcycle']['occupied'] == 0
    assert occupancy['motorcycle']['available'] == 2
    assert occupancy['compact']['capacity'] == 2
    assert occupancy['compact']['occupied'] == 1
    assert occupancy['compact']['available'] == 1
    assert occupancy['large']['capacity'] == 2
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 2

    lot.check_in("C-2", "car", 1.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['capacity'] == 2
    assert occupancy['motorcycle']['occupied'] == 0
    assert occupancy['motorcycle']['available'] == 2
    assert occupancy['compact']['capacity'] == 2
    assert occupancy['compact']['occupied'] == 2
    assert occupancy['compact']['available'] == 0
    assert occupancy['large']['capacity'] == 2
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 2

def test_occupancy_increases_after_checkout():
    lot = ParkingLot(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1.0)
    lot.check_out("C-1", 2.0)  # Assuming entry time was at 1.0
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['capacity'] == 1
    assert occupancy['motorcycle']['occupied'] == 0
    assert occupancy['motorcycle']['available'] == 1
    assert occupancy['compact']['capacity'] == 1
    assert occupancy['compact']['occupied'] == 0
    assert occupancy['compact']['available'] == 1
    assert occupancy['large']['capacity'] == 1
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 1