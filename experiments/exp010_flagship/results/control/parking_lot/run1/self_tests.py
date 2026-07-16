import pytest
from solution import ParkingLot

def test_configure_lot_with_valid_configuration():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=10,
        compact_spots=20,
        large_spots=5,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    assert lot is not None  # Ensure the lot is configured correctly

def test_configure_lot_with_negative_spot_count():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure_lot(
            motorcycle_spots=10,
            compact_spots=-1,  # Invalid spot count
            large_spots=5,
            rates={
                "motorcycle": 1.0,
                "car": 2.0,
                "bus": 5.0
            }
        )
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configure_lot_with_no_spots():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure_lot(
            motorcycle_spots=0,
            compact_spots=0,
            large_spots=0,
            rates={
                "motorcycle": 1.0,
                "car": 2.0,
                "bus": 5.0
            }
        )
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configure_lot_with_missing_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure_lot(
            motorcycle_spots=10,
            compact_spots=20,
            large_spots=5,
            rates={
                "motorcycle": 1.0,
                "car": 2.0,
                # Missing rate for bus
            }
        )
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_configure_lot_with_non_positive_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure_lot(
            motorcycle_spots=10,
            compact_spots=20,
            large_spots=5,
            rates={
                "motorcycle": 1.0,
                "car": 0.0,  # Non-positive rate
                "bus": 5.0
            }
        )
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_motorcycle_check_in():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket['vehicle_id'] == "M-1"
    assert ticket['spot_type'] == "motorcycle"

def test_car_check_in():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    ticket = lot.check_in("C-1", "car", 1000.0)
    assert ticket['vehicle_id'] == "C-1"
    assert ticket['spot_type'] == "compact"

def test_bus_check_in():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    ticket = lot.check_in("B-1", "bus", 1000.0)
    assert ticket['vehicle_id'] == "B-1"
    assert ticket['spot_type'] == "large"

def test_check_in_no_available_spot_for_car():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=0,
        compact_spots=0,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    lot.check_in("B-1", "bus", 1000.0)  # Bus takes the last spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1000.0)  # Car can't find a spot
    assert str(excinfo.value) == "no available spot for [car]"

def test_check_in_already_parked_vehicle():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    lot.check_in("C-1", "car", 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1005.0)  # Attempt to check in again
    assert str(excinfo.value) == "vehicle [C-1] is already parked"

def test_checkout_vehicle():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1100.0)
    assert receipt['vehicle_id'] == "C-1"
    assert receipt['billed_hours'] == 1  # 1000 to 1100 is 1 hour
    assert receipt['fee'] == 2.0  # 1 hour * rate of car (2.0)

def test_checkout_not_parked_vehicle():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("ghost", 1100.0)  # Ghost vehicle not checked in
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_checkout_exit_time_before_entry_time():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    lot.check_in("C-1", "car", 1100.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("C-1", 1000.0)  # Invalid exit time
    assert str(excinfo.value) == "exit_time [1000.0] is before entry_time [1100.0]"

def test_report_occupancy():
    lot = ParkingLot()
    lot.configure_lot(
        motorcycle_spots=1,
        compact_spots=1,
        large_spots=1,
        rates={
            "motorcycle": 1.0,
            "car": 2.0,
            "bus": 5.0
        }
    )
    lot.check_in("C-1", "car", 1100.0)
    occupancy = lot.report_occupancy()
    assert occupancy['motorcycle']['available'] == 1
    assert occupancy['compact']['available'] == 0
    assert occupancy['large']['available'] == 1
    assert occupancy['motorcycle']['occupied'] == 0
    assert occupancy['compact']['occupied'] == 1
    assert occupancy['large']['occupied'] == 0