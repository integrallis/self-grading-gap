import pytest
from solution import ParkingLot

def test_configuring_lot_negative_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spot_counts={"motorcycle": 1, "compact": -1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configuring_lot_no_spots():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spot_counts={"motorcycle": 0, "compact": 0, "large": 0}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configuring_lot_missing_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0})  # missing bus rate
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_configuring_lot_non_positive_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 0.0, "bus": 5.0})
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_motorcycle_parks_in_motorcycle_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "motorcycle"

def test_motorcycle_falls_back_to_compact_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 0, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "compact"

def test_motorcycle_falls_back_to_large_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 0, "compact": 0, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "large"

def test_car_parks_in_compact_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    ticket = lot.check_in(vehicle_id="C-1", vehicle_type="car", entry_time=1010.0)
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "compact"

def test_car_fallback_to_large_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 0, "compact": 0, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="C-1", vehicle_type="car", entry_time=1000.0)
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "large"

def test_bus_parks_in_large_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 0, "compact": 0, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in(vehicle_id="B-1", vehicle_type="bus", entry_time=1000.0)
    assert ticket["vehicle_id"] == "B-1"
    assert ticket["spot_type"] == "large"

def test_car_refused_when_only_motorcycle_spots_available():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 0, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in(vehicle_id="C-1", vehicle_type="car", entry_time=1010.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_bus_refused_when_no_large_spots_available():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 0}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="C-1", vehicle_type="car", entry_time=1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in(vehicle_id="B-1", vehicle_type="bus", entry_time=1010.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_full_lot_reports_full_state():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    lot.check_in(vehicle_id="C-1", vehicle_type="car", entry_time=1010.0)
    lot.check_in(vehicle_id="B-1", vehicle_type="bus", entry_time=1020.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in(vehicle_id="E-1", vehicle_type="car", entry_time=1030.0)
    assert str(excinfo.value) == "parking lot is full"

def test_checkout_frees_spot():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    lot.check_out(vehicle_id="M-1", exit_time=1100.0)
    assert not lot.is_parked("M-1")

def test_checkout_not_parked():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_out(vehicle_id="ghost", exit_time=1100.0)
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_checkout_updates_occupancy():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    lot.check_out(vehicle_id="M-1", exit_time=1100.0)
    ticket = lot.check_in(vehicle_id="C-1", vehicle_type="car", entry_time=1110.0)
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "compact"

def test_duplicate_check_in():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1010.0)
    assert str(excinfo.value) == "vehicle [M-1] is already parked"

def test_billing_for_stay():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    receipt = lot.check_out(vehicle_id="M-1", exit_time=1200.0)  # 2 hours
    assert receipt["vehicle_id"] == "M-1"
    assert receipt["vehicle_type"] == "motorcycle"
    assert receipt["spot_type"] == "motorcycle"
    assert receipt["entry_time"] == 1000.0
    assert receipt["exit_time"] == 1200.0
    assert receipt["billed_hours"] == 2  # 2 hours
    assert receipt["fee"] == 2.0  # 2 hours * 1.0 per hour

def test_exit_time_before_entry_time():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out(vehicle_id="M-1", exit_time=999.0)
    assert str(excinfo.value) == "exit_time [999.0] is before entry_time [1000.0]"

def test_report_occupancy():
    lot = ParkingLot(spot_counts={"motorcycle": 1, "compact": 1, "large": 1}, hourly_rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["capacity"] == 1
    assert occupancy["motorcycle"]["occupied"] == 0
    assert occupancy["motorcycle"]["available"] == 1
    assert occupancy["compact"]["capacity"] == 1
    assert occupancy["compact"]["occupied"] == 0
    assert occupancy["compact"]["available"] == 1
    assert occupancy["large"]["capacity"] == 1
    assert occupancy["large"]["occupied"] == 0
    assert occupancy["large"]["available"] == 1
    
    lot.check_in(vehicle_id="M-1", vehicle_type="motorcycle", entry_time=1000.0)
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["capacity"] == 1
    assert occupancy["motorcycle"]["occupied"] == 1
    assert occupancy["motorcycle"]["available"] == 0
    assert occupancy["compact"]["capacity"] == 1
    assert occupancy["compact"]["occupied"] == 0
    assert occupancy["compact"]["available"] == 1
    assert occupancy["large"]["capacity"] == 1
    assert occupancy["large"]["occupied"] == 0
    assert occupancy["large"]["available"] == 1
    
    lot.check_out(vehicle_id="M-1", exit_time=1100.0)
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["capacity"] == 1
    assert occupancy["motorcycle"]["occupied"] == 0
    assert occupancy["motorcycle"]["available"] == 1
    assert occupancy["compact"]["capacity"] == 1
    assert occupancy["compact"]["occupied"] == 0
    assert occupancy["compact"]["available"] == 1
    assert occupancy["large"]["capacity"] == 1
    assert occupancy["large"]["occupied"] == 0
    assert occupancy["large"]["available"] == 1