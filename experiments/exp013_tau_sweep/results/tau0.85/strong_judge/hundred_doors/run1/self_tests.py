# test_solution.py

import pytest
from solution import report_open_positions, report_open_closed_indicators, report_marker_string

def test_report_open_positions_with_100_doors():
    # 100 doors will have doors at perfect-square positions open: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100
    expected_open_positions = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    assert report_open_positions(100) == expected_open_positions

def test_report_open_positions_with_50_doors():
    # 50 doors will have doors at perfect-square positions open: 1, 4, 9, 16, 25, 36, 49
    expected_open_positions = [1, 4, 9, 16, 25, 36, 49]
    assert report_open_positions(50) == expected_open_positions

def test_report_open_positions_with_10_doors():
    # 10 doors will have doors at perfect-square positions open: 1, 4, 9
    expected_open_positions = [1, 4, 9]
    assert report_open_positions(10) == expected_open_positions

def test_report_open_positions_with_1_door():
    # 1 door will be open after the only walk
    expected_open_positions = [1]
    assert report_open_positions(1) == expected_open_positions

def test_report_open_positions_with_2_doors():
    # 2 doors will have door 1 open and door 2 closed
    expected_open_positions = [1]
    assert report_open_positions(2) == expected_open_positions

def test_report_open_positions_with_0_doors():
    # 0 doors yield an empty list of open positions
    expected_open_positions = []
    assert report_open_positions(0) == expected_open_positions

def test_report_open_positions_with_negative_doors():
    # Negative door count should raise an error with a specific message
    with pytest.raises(Exception) as excinfo:
        report_open_positions(-1)
    assert str(excinfo.value) == "door count must be non-negative"

def test_report_open_closed_indicators_with_10_doors():
    # Testing the list of open/closed indicators for 10 doors
    expected_indicators = [True, False, False, True, False, False, False, False, True, False]  # Open/Closed indicators
    assert report_open_closed_indicators(10) == expected_indicators

def test_report_marker_string_with_10_doors():
    # Testing the string representation for 10 doors
    expected_string = "@##@####@#"
    assert report_marker_string(10) == expected_string

def test_report_open_positions_with_0_doors_empty_string():
    # 0 doors yield an empty string
    expected_string = ""
    assert report_marker_string(0) == expected_string

def test_report_open_positions_with_0_doors_empty_indicators():
    # 0 doors yield an empty list of open/closed indicators
    expected_indicators = []
    assert report_open_closed_indicators(0) == expected_indicators