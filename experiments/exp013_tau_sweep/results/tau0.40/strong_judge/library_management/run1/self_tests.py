import pytest
from solution import Library, Member

def test_add_new_copy():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    assert library.get_available_copies("978-1") == 1  # 1 new copy added

def test_multiple_copies():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_copies("978-1") == 2  # 2 copies added

def test_catalogue_record():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    title_info = library.get_title_info("978-1")
    assert title_info[0] == "978-1"  # Check ISBN
    assert title_info[1] == "Book Title"  # Check title
    assert title_info[2] == "Fiction"  # Check category
    assert title_info[3] == "Shelf A"  # Check shelf location

def test_copy_identifier():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_copy_identifier("978-1", 1) == "978-1/1"  # First copy identifier
    assert library.get_copy_identifier("978-1", 2) == "978-1/2"  # Second copy identifier

def test_unknown_copy_identifier():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:  # General exception since specific type not defined
        library.get_copy_status("978-1/3")  # Unknown copy identifier
    assert "Unknown copy identifier: 978-1/3" in str(excinfo.value)  # Check for error content

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.remove_copy("978-1/1")  # Remove an available copy
    assert library.get_available_copies("978-1") == 0  # Count should decrease

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:  # General exception since specific type not defined
        library.remove_copy("978-1/1")  # Attempt to remove a checked out copy
    assert "not available for removal" in str(excinfo.value)  # Check for error content

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    checkout_info = library.checkout("978-1", member)
    assert checkout_info['due_date'] is not None  # Due date should be set
    assert library.get_available_copies("978-1") == 0  # Available copy count should decrease
    due_date = checkout_info['due_date']
    assert due_date == checkout_info['checkout_day'] + 14  # Loan period is 14 days by default

def test_checkout_no_available_copies():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    member = Member("member1")
    library.register_member(member)
    with pytest.raises(Exception) as excinfo:  # General exception since specific type not defined
        library.checkout("978-1", member)  # No available copies
    assert "No copies of 978-1 are available" in str(excinfo.value)  # Check for error content

def test_checkout_unknown_title():
    library = Library()
    member = Member("member1")
    library.register_member(member)
    with pytest.raises(Exception) as excinfo:  # General exception since specific type not defined
        library.checkout("978-1", member)  # ISBN not in catalogue
    assert "Unknown book: 978-1" in str(excinfo.value)  # Check for error content

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    checkout_info = library.checkout("978-1", member)
    fine = library.return_copy("978-1/1", member)  # Return on time
    assert fine == 0  # No fine for on-time return
    assert library.get_available_copies("978-1") == 1  # Copy should be available again

def test_return_late():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    library.set_fine_rate(0.50)  # Assuming a method to set fine rate
    # Simulate late return by controlling the return logic
    fine = library.return_copy("978-1/1", member, days_late=3)  # Return 3 days late
    assert fine == 0.50 * 3  # Fine should be 0.50 * 3 days late

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    with pytest.raises(Exception) as excinfo:  # General exception since specific type not defined
        library.return_copy("978-1/1", member)  # Attempting to return a non-checked-out copy
    assert "not checked out" in str(excinfo.value)  # Check for error content

def test_reserve_title():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)
    library.register_member(member2)
    library.add_copy("978-1")
    library.checkout("978-1", member1)  # Member1 checks out the only copy
    library.reserve("978-1", member2)  # Member2 reserves the copy
    # Check that the reservation was successful in some observable way
    assert library.get_reserved_status("978-1", member2)  # Assuming method to check reservation status

def test_return_reserved_copy():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)
    library.register_member(member2)
    library.add_copy("978-1")
    library.checkout("978-1", member1)  # Member1 checks out the only copy
    library.reserve("978-1", member2)  # Member2 reserves the copy
    library.return_copy("978-1/1", member1)  # Member1 returns the copy
    assert library.get_copy_status("978-1/1") == "reserved"  # Check status of copy
    # Verify that member2 was notified or the reservation queue updated accordingly

def test_cancel_reservation():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    member = Member("member1")
    library.register_member(member)
    library.add_copy("978-1")
    library.reserve("978-1", member)
    library.cancel_reservation("978-1", member)  # Cancel reservation
    assert library.get_available_copies("978-1") == 1  # Copy should now be available

def test_cancel_non_existing_reservation():
    library = Library()
    library.add_title("978-1", "Book Title", "Fiction", "Shelf A")
    member = Member("member1")
    library.register_member(member)
    with pytest.raises(Exception) as excinfo:  # General exception since specific type not defined
        library.cancel_reservation("978-1", member)  # No reservation to cancel
    assert "Member has no reservation for ISBN 978-1" in str(excinfo.value)  # Check for error content