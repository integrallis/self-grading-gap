# test_library_circulation.py

import pytest
from solution import Library, Member

# US-1: Catalogue and inventory

def test_add_copy_available():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    assert library.check_copy_status(copy_id) == "available"  # AC-1.1

def test_add_multiple_copies():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.available_copies_count("978-1") == 2  # AC-1.2

def test_catalogue_record():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    title_info = library.get_title_info("978-1")
    assert title_info[0] == "978-1"  # ISBN
    assert title_info[1] == "Test Title"  # Title
    assert title_info[2] == "Fiction"  # Category
    assert title_info[3] == "A1"  # Shelf location  # AC-1.3

def test_copy_identifier():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id_1 = library.add_copy("978-1")
    copy_id_2 = library.add_copy("978-1")
    assert copy_id_1 == "978-1/1"  # AC-1.4
    assert copy_id_2 == "978-1/2"  # AC-1.4

def test_unknown_copy_identifier():
    library = Library()
    with pytest.raises(Exception) as excinfo:  # Error expected for unknown identifier
        library.check_copy_status("unknown-id")  # AC-1.5
    assert "unknown-id" in str(excinfo.value)  # Check error message

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    library.remove_copy(copy_id)
    assert library.available_copies_count("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:  # Error expected for not available for removal
        library.remove_copy(copy_id)  # AC-1.7
    assert "not available for removal" in str(excinfo.value)  # Check error message

# US-2: Checkout

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    library.add_copy("978-1")
    member = Member("member-1")
    checkout_info = library.checkout("978-1", member)
    assert checkout_info['due_date'] is not None  # Due date must be set  # AC-2.1
    assert checkout_info['due_date'] == checkout_info['checkout_date'] + 14  # Check due date calculation
    assert library.check_copy_status("978-1/1") == "checked_out"  # AC-2.3

def test_checkout_no_free_copies():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:  # Error expected for no copies available
        library.checkout("978-1", Member("member-2"))  # AC-2.5
    assert "No copies of 978-1 are available" in str(excinfo.value)  # Check error message

def test_checkout_unknown_isbn():
    library = Library()
    with pytest.raises(Exception) as excinfo:  # Error expected for unknown ISBN
        library.checkout("978-2", Member("member-1"))  # AC-2.6
    assert "unknown-book error" in str(excinfo.value)  # Check error message

def test_checkout_unregistered_member():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:  # Error expected for unknown member
        library.checkout("978-1", Member("member-2"))  # AC-2.7
    assert "unknown-member error" in str(excinfo.value)  # Check error message

def test_checkout_with_another_available_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id_1 = library.add_copy("978-1")
    copy_id_2 = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)  # Checkout first copy
    assert library.check_copy_status(copy_id_2) == "available"  # Ensure second copy is still available
    library.checkout("978-1", Member("member-2"))  # Checkout second copy should succeed

# US-3: Returns and fines

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    fine = library.return_copy(copy_id, member)
    assert fine == 0  # On-time return should incur no fine  # AC-3.1
    assert library.check_copy_status(copy_id) == "available"  # AC-3.3

def test_return_late():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    library.advance_time(days=17)  # Simulate 17 days passing for a 14-day loan
    fine = library.return_copy(copy_id, member)  # AC-3.2
    assert fine == 1.50  # 3 days late at a configured rate of 0.50 per day

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:  # Error expected for not checked out
        library.return_copy(copy_id, Member("member-1"))  # AC-3.4
    assert "not checked out" in str(excinfo.value)  # Check error message

# US-4: Reservations and holds

def test_reserve_title_unavailable():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member-1")
    library.reserve("978-1", member)
    # Direct verification not possible as specified; ensuring no exceptions occur

def test_checkout_reserved_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    library.reserve("978-1", Member("member-2"))
    library.return_copy(copy_id, member)  # Now member-2 should be able to check out the previously reserved copy
    checkout_info = library.checkout("978-1", Member("member-2"))  # AC-4.3
    assert library.check_copy_status(copy_id) == "checked_out"  # Check that copy is checked out

def test_reserve_same_title_twice():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member-1")
    library.reserve("978-1", member)
    with pytest.raises(Exception) as excinfo:  # Error expected for duplicate reservation
        library.reserve("978-1", member)  # AC-4.6
    assert "already has a reservation" in str(excinfo.value)  # Check error message

def test_reserve_while_copy_available():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.reserve("978-1", member)
    assert library.check_copy_status(copy_id) == "reserved"  # AC-4.5

def test_collect_specific_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id_1 = library.add_copy("978-1")
    copy_id_2 = library.add_copy("978-1")
    member_1 = Member("member-1")
    member_2 = Member("member-2")
    library.reserve("978-1", member_1)
    library.reserve("978-1", member_2)
    library.return_copy(copy_id_1, member_1)  # member_1 collects the held copy
    library.checkout(copy_id_1, member_1)  # AC-4.8
    assert library.check_copy_status(copy_id_1) == "checked_out"  # member_1 should now have it checked out

# US-5: Cancellations and hold expiry

def test_cancel_queued_reservation():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member-1")
    library.reserve("978-1", member)
    library.cancel_reservation("978-1", member)
    # Direct verification not possible as specified; ensuring no exceptions occur

def test_cancel_reservation_after_hold():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member-1")
    library.reserve("978-1", member)
    copy_id = library.add_copy("978-1")
    library.return_copy(copy_id, member)
    library.cancel_reservation("978-1", member)
    assert library.check_copy_status(copy_id) == "available"  # AC-5.2

def test_cancel_nonexistent_reservation():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member-1")
    with pytest.raises(Exception) as excinfo:  # Error expected for nonexistent reservation
        library.cancel_reservation("978-1", member)  # AC-5.3
    assert "has no reservation for" in str(excinfo.value)  # Check error message

def test_cancel_other_member_hold():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member_1 = Member("member-1")
    member_2 = Member("member-2")
    library.reserve("978-1", member_1)
    with pytest.raises(Exception) as excinfo:  # Error expected for cannot cancel other's hold
        library.cancel_reservation("978-1", member_2)  # AC-5.4
    assert "cannot cancel" in str(excinfo.value)  # Check error message

def test_lapse_uncollected_hold():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member-1")
    library.reserve("978-1", member)
    library.advance_time(days=4)  # Lapse after 3 days
    # Direct verification not possible as specified; ensuring no exceptions occur

def test_lapse_notification_for_next_member():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member_1 = Member("member-1")
    member_2 = Member("member-2")
    library.reserve("978-1", member_1)
    library.reserve("978-1", member_2)
    library.advance_time(days=4)  # Lapse after 3 days
    # Direct verification not possible as specified; ensuring no exceptions occur