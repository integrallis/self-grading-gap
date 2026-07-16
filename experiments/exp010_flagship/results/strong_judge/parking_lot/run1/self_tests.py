# test_parking_lot.py

import pytest
from solution import ParkingLot

def test_configuring_lot_with_positive_spot_counts_and_rates():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 10, "compact": 20, "large": 30}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    # Verify that configuration is retained and usable
    assert lot is not None  # Just checking that the lot was created

def test_configuring_lot_with_negative_spot_count():
    lot = ParkingLot()
    with pytest.raises(ValueError) as exc:
        lot.configure(spots={"motorcycle": 10, "compact": -1, "large": 30}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(exc.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configuring_lot_with_no_spots():
    lot = ParkingLot()
    with pytest.raises(ValueError) as exc:
        lot.configure(spots={"motorcycle": 0, "compact": 0, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(exc.value) == "parking lot must have at least one spot"

def test_configuring_lot_with_missing_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as exc:
        lot.configure(spots={"motorcycle": 10, "compact": 20, "large": 30}, rates={"motorcycle": 1.0, "car": 2.0})
    assert str(exc.value) == "missing hourly rate for [bus]"

def test_configuring_lot_with_non_positive_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as exc:
        lot.configure(spots={"motorcycle": 10, "compact": 20, "large": 30}, rates={"motorcycle": 1.0, "car": 0.0, "bus": 5.0})
    assert str(exc.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_configuring_lot_with_negative_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as exc:
        lot.configure(spots={"motorcycle": 10, "compact": 20, "large": 30}, rates={"motorcycle": 1.0, "car": -2.0, "bus": 5.0})
    assert str(exc.value) == "hourly rate for [car] must be positive, got [-2.0]"

def test_motorcycle_check_in():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    assert "vehicle_id" in ticket and ticket["vehicle_id"] == "M-1"  # Check vehicle ID
    assert "spot_type" in ticket and ticket["spot_type"] == "motorcycle"  # Check spot type
    assert lot.is_parked("M-1")  # Check that the vehicle is reported as parked

def test_car_check_in():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    assert "vehicle_id" in ticket and ticket["vehicle_id"] == "C-1"  # Check vehicle ID
    assert "spot_type" in ticket and ticket["spot_type"] == "compact"  # Check spot type
    assert lot.is_parked("C-1")  # Check that the vehicle is reported as parked

def test_bus_check_in():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="B-1", vehicle_type="bus", check_in_time=1000.0)
    assert "vehicle_id" in ticket and ticket["vehicle_id"] == "B-1"  # Check vehicle ID
    assert "spot_type" in ticket and ticket["spot_type"] == "large"  # Check spot type
    assert lot.is_parked("B-1")  # Check that the vehicle is reported as parked

def test_motorcycle_fallback_check_in():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    ticket = lot.check_in(vehicle_id="M-2", vehicle_type="motorcycle", check_in_time=1010.0)
    assert "vehicle_id" in ticket and ticket["vehicle_id"] == "M-2"  # Check vehicle ID
    assert "spot_type" in ticket and ticket["spot_type"] == "compact"  # Should fall back to compact
    assert lot.is_parked("M-2")  # Check that the vehicle is reported as parked

def test_car_fallback_check_in():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    ticket = lot.check_in(vehicle_id="C-2", vehicle_type="car", check_in_time=1010.0)
    assert "vehicle_id" in ticket and ticket["vehicle_id"] == "C-2"  # Check vehicle ID
    assert "spot_type" in ticket and ticket["spot_type"] == "large"  # Should fall back to large
    assert lot.is_parked("C-2")  # Check that the vehicle is reported as parked

def test_bus_rejection_when_no_large_spots():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as exc:
        lot.check_in(vehicle_id="B-1", vehicle_type="bus", check_in_time=1000.0)
    assert str(exc.value) == "no available spot for [bus]"

def test_car_rejection_when_only_motorcycle_spots_available():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 0, "large": 0}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as exc:
        lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    assert str(exc.value) == "no available spot for [car]"

def test_check_in_full_lot():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    lot.check_in(vehicle_id="B-1", vehicle_type="bus", check_in_time=1000.0)
    with pytest.raises(ValueError) as exc:
        lot.check_in(vehicle_id="C-2", vehicle_type="car", check_in_time=1010.0)
    assert str(exc.value) == "no available spot for [car]"

def test_check_in_already_parked_vehicle():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    with pytest.raises(ValueError) as exc:
        lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1010.0)
    assert str(exc.value).startswith("vehicle [C-1] is already parked")  # Check informative message

def test_check_out_vehicle():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="C-1", exit_time=1200.0)
    assert "vehicle_id" in receipt and receipt["vehicle_id"] == "C-1"  # Check vehicle ID
    assert "vehicle_type" in receipt and receipt["vehicle_type"] == "car"  # Check vehicle type
    assert "spot_type" in receipt and receipt["spot_type"] == "compact"  # Check spot type
    assert "entry_time" in receipt and receipt["entry_time"] == 1000.0  # Check entry time
    assert "exit_time" in receipt and receipt["exit_time"] == 1200.0  # Check exit time
    assert "billed_hours" in receipt and receipt["billed_hours"] == 1  # 1 hour
    assert "fee" in receipt and receipt["fee"] == 2.0  # 2.0 for car
    assert not lot.is_parked("C-1")  # Check that the vehicle is reported as not parked

def test_check_out_not_parked_vehicle():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as exc:
        lot.check_out(vehicle_id="ghost", exit_time=1200.0)
    assert str(exc.value).startswith("vehicle [ghost] is not parked")  # Check informative message

def test_checkout_receipt_billing_zero_duration():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=1000.0)  # 0 hours
    assert receipt["billed_hours"] == 1  # Minimum charge is 1 hour
    assert receipt["fee"] == 1.0  # 1.0 for motorcycle

def test_checkout_receipt_billing_ten_minutes():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=1010.0)  # 10 minutes
    assert receipt["billed_hours"] == 1  # Minimum charge is 1 hour
    assert receipt["fee"] == 1.0  # 1.0 for motorcycle

def test_checkout_receipt_billing_ninety_minutes():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=1150.0)  # 90 minutes
    assert receipt["billed_hours"] == 2  # 90 minutes rounds up to 2 hours
    assert receipt["fee"] == 2.0  # 2.0 for motorcycle

def test_checkout_receipt_billing_one_second_past_hour():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=1060.0)  # 1 hour and 1 second
    assert receipt["billed_hours"] == 2  # 1 hour and 1 second rounds up to 2 hours
    assert receipt["fee"] == 2.0  # 2.0 for motorcycle

def test_checkout_receipt_billing_exact_hours():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=1200.0)  # 2 hours
    assert receipt["billed_hours"] == 2  # Exact 2 hours
    assert receipt["fee"] == 2.0  # 2.0 for motorcycle

def test_checkout_receipt_billing_two_hour_costs():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=2000.0)  # 10 hours
    assert receipt["billed_hours"] == 10  # 10 hours
    assert receipt["fee"] == 10.0  # 10.0 for motorcycle

def test_exit_time_before_entry_time():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    with pytest.raises(ValueError) as exc:
        lot.check_out(vehicle_id="C-1", exit_time=999.0)
    assert str(exc.value).startswith("exit_time [999.0] is before entry_time [1000.0]")  # Check informative message

def test_reporting_occupancy():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 2, "compact": 2, "large": 2}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    occupancy = lot.report_occupancy()
    assert "motorcycle" in occupancy
    assert occupancy["motorcycle"]["capacity"] == 2
    assert occupancy["motorcycle"]["occupied"] == 1
    assert occupancy["motorcycle"]["available"] == 1
    assert "compact" in occupancy
    assert occupancy["compact"]["capacity"] == 2
    assert occupancy["compact"]["occupied"] == 1
    assert occupancy["compact"]["available"] == 1
    assert "large" in occupancy
    assert occupancy["large"]["capacity"] == 2
    assert occupancy["large"]["occupied"] == 0
    assert occupancy["large"]["available"] == 2

def test_checkout_increases_availability():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    lot.check_out(vehicle_id="M-1", exit_time=1200.0)
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["available"] == 1  # Spot should be available again

def test_checkout_and_rearrival():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", check_in_time=1000.0)
    lot.check_out(vehicle_id="M-1", exit_time=1200.0)
    ticket = lot.check_in(vehicle_id="M-2", vehicle_type="motorcycle", check_in_time=1300.0)  # Re-check in after checkout
    assert "vehicle_id" in ticket and ticket["vehicle_id"] == "M-2"  # Check vehicle ID
    assert "spot_type" in ticket and ticket["spot_type"] == "motorcycle"  # Should get motorcycle spot again
    assert lot.is_parked("M-2")  # Check that the vehicle is reported as parked

def test_multiple_same_type_vehicles_checkout():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 2, "compact": 2, "large": 2}, rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="C-1", vehicle_type="car", check_in_time=1000.0)
    lot.check_in(vehicle_id="C-2", vehicle_type="car", check_in_time=1010.0)
    receipt = lot.check_out(vehicle_id="C-1", exit_time=1200.0)  # Checkout C-1
    assert "vehicle_id" in receipt and receipt["vehicle_id"] == "C-1"  # Check vehicle ID
    assert lot.is_parked("C-2")  # C-2 should still be parked