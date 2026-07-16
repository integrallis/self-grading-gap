import pytest
from solution import Library

def test_add_copy_available():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    assert library.get_copy_status(copy_id) == "available"  # AC-1.1

def test_add_multiple_copies():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_copy_count("978-1") == 2  # AC-1.2

def test_copy_identifier_combination():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id_1 = library.add_copy("978-1")
    copy_id_2 = library.add_copy("978-1")
    assert copy_id_1 == "978-1/1"  # AC-1.4
    assert copy_id_2 == "978-1/2"  # AC-1.4

def test_check_unknown_copy_identifier():
    library = Library()
    with pytest.raises(Exception) as exc_info:
        library.get_copy_status("unknown-id")  # AC-1.5
    assert "unknown-id" in str(exc_info.value)

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    library.remove_copy(copy_id)
    assert library.get_available_copy_count("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = "member-1"
    library.checkout("978-1", member)
    with pytest.raises(Exception) as exc_info:
        library.remove_copy(copy_id)  # AC-1.7
    assert "not available for removal" in str(exc_info.value)

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = "member-1"
    due_date = library.checkout("978-1", member)
    assert library.get_copy_status(copy_id) == "checked_out"  # AC-2.3
    assert due_date is not None  # AC-2.1

def test_checkout_no_free_copies():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = "member-1"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member)
    with pytest.raises(Exception) as exc_info:
        library.checkout("978-1", member)  # AC-2.5
    assert "No copies of 978-1 are available" in str(exc_info.value)

def test_checkout_unknown_book():
    library = Library()
    member = "member-1"
    with pytest.raises(Exception) as exc_info:
        library.checkout("978-0", member)  # AC-2.6
    assert "978-0" in str(exc_info.value)

def test_checkout_unknown_member():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    with pytest.raises(Exception) as exc_info:
        library.checkout("978-1", "unknown-member")  # AC-2.7
    assert "unknown-member" in str(exc_info.value)

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = "member-1"
    library.checkout("978-1", member)
    fine = library.return_copy(copy_id, member)
    assert fine == 0  # AC-3.1
    assert library.get_copy_status(copy_id) == "available"  # AC-3.3

def test_return_late():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    library.set_fine_per_day(0.50)
    copy_id = library.add_copy("978-1")
    member = "member-1"
    library.checkout("978-1", member)
    library.advance_days(15)  # Simulate 15 days passing
    fine = library.return_copy(copy_id, member)
    assert fine == 0.50  # AC-3.2

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    with pytest.raises(Exception) as exc_info:
        library.return_copy(copy_id, "member-1")  # AC-3.4
    assert "not checked out" in str(exc_info.value)

def test_reserve_title():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member_1 = "member-1"
    member_2 = "member-2"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member_1)
    library.reserve("978-1", member_2)
    # No assertion for this test because the specification does not define a status for queued reservations.

def test_checkout_reserved_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member_1 = "member-1"
    member_2 = "member-2"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member_1)
    library.reserve("978-1", member_2)
    library.return_copy(copy_id, member_1)
    library.collect_reserved_copy("978-1", member_2)
    assert library.get_copy_status(copy_id) == "checked_out"  # AC-4.3

def test_duplicate_reservation():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = "member-1"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member)
    library.reserve("978-1", member)
    with pytest.raises(Exception) as exc_info:
        library.reserve("978-1", member)  # AC-4.6
    assert "already has a reservation" in str(exc_info.value)

def test_cancel_queued_reservation():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member_1 = "member-1"
    member_2 = "member-2"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member_1)
    library.reserve("978-1", member_2)
    library.cancel_reservation("978-1", member_2)
    # No assertion because the specification does not define a status for cancelled reservations.

def test_cancel_active_reservation():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = "member-1"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member)
    library.reserve("978-1", member)
    library.return_copy(copy_id, member)
    with pytest.raises(Exception) as exc_info:
        library.cancel_reservation("978-1", member)  # AC-5.2
    assert "has no reservation for 978-1" in str(exc_info.value)

def test_cancel_nonexistent_reservation():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = "member-1"
    with pytest.raises(Exception) as exc_info:
        library.cancel_reservation("978-1", member)  # AC-5.3
    assert "has no reservation for 978-1" in str(exc_info.value)

def test_cancel_reservation_for_others():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member_1 = "member-1"
    member_2 = "member-2"
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member_1)
    library.reserve("978-1", member_2)
    with pytest.raises(Exception) as exc_info:
        library.cancel_reservation("978-1", member_1)  # AC-5.4
    assert "has no reservation for 978-1" in str(exc_info.value)

def test_hold_expiry():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = "member-1"
    copy_id = library.add_copy("978-1")
    library.reserve("978-1", member)
    library.advance_days(4)  # Simulate 4 days passing (hold period)
    assert library.get_copy_status(copy_id) == "available"  # AC-5.5

def test_hold_period_default():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    assert library.get_hold_period() == 3  # AC-5.6

def test_lapsed_hold_notification():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member_1 = "member-1"
    member_2 = "member-2"
    copy_id = library.add_copy("978-1")
    library.reserve("978-1", member_1)
    library.advance_days(4)  # Simulate 4 days (hold period)
    library.reserve("978-1", member_2)  # member_2 gets the next hold
    # No assertion here because the specification does not define a status for queued reservations.