import pytest
from solution import Library, Member

def test_add_new_copy_available():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    assert library.get_available_copies("978-1") == 1  # Newly added copy is available

def test_add_multiple_copies():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_copies("978-1") == 2  # Two copies should both be tracked

def test_catalogue_record():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    title_info = library.get_catalogue_info("978-1")
    assert "978-1" in title_info  # ISBN should be retrievable
    assert "Title One" in title_info  # Title should be retrievable
    assert "Fiction" in title_info  # Category should be retrievable
    assert "Shelf A" in title_info  # Shelf location should be retrievable

def test_copy_identifier():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_copy_identifier("978-1", 1) == "978-1/1"  # First copy identifier
    assert library.get_copy_identifier("978-1", 2) == "978-1/2"  # Second copy identifier

def test_unknown_copy_identifier():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.get_copy_status("978-1/3")  # Requesting unknown copy identifier
    assert "978-1/3" in str(excinfo.value)  # Error must name the unknown identifier

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.remove_copy("978-1/1")  # Remove first available copy
    assert library.get_available_copies("978-1") == 0  # Available count should decrease

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout("978-1", member)  # Register member implicitly during checkout
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.remove_copy("978-1/1")  # Attempt to remove checked out copy
    assert "not available for removal" in str(excinfo.value)

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)  # Explicit registration step
    due_date = library.checkout("978-1", member)
    # Due date is today + 14 days
    assert due_date is not None  # Due date is set

def test_checkout_with_one_copy_checked_out():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)  # Register members
    library.register_member(member2)
    library.checkout("978-1", member1)  # member1 checks out one copy
    library.checkout("978-1", member2)  # member2 checks out another copy
    assert library.get_copy_status("978-1/1") == "checked_out"  # Status should be checked out
    assert library.get_copy_status("978-1/2") == "checked_out"  # Status should be checked out

def test_checkout_no_free_copies():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)  # Register member
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.checkout("978-1", member)  # No copies available
    assert "No copies of 978-1 are available" in str(excinfo.value)

def test_checkout_unknown_isbn():
    library = Library()
    member = Member("member1")
    library.register_member(member)  # Register member
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.checkout("978-1", member)  # ISBN not in catalogue
    assert "978-1" in str(excinfo.value)  # Error must name the unknown ISBN

def test_checkout_unregistered_member():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member2")  # Unregistered member
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.checkout("978-1", member)  # Attempt to checkout
    assert "unknown member" in str(excinfo.value)  # Error must indicate unknown member

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)  # Register member
    library.checkout("978-1", member)
    return_fee = library.return_copy("978-1/1", member)  # Returned on time
    assert return_fee == 0  # No fee for on-time return

def test_return_late():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)  # Register member
    library.checkout("978-1", member)
    library.configure_fine_rate(0.50)  # Configured fine rate
    return_fee = library.return_copy("978-1/1", member, overdue_days=3)  # Returned 3 days late
    assert return_fee == 1.50  # Fee should be 3 * 0.50 = 1.50

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.return_copy("978-1/1", member)  # Not checked out
    assert "not checked out" in str(excinfo.value)

def test_reserve_title():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)  # Register members
    library.register_member(member2)
    library.add_copy("978-1")
    library.checkout("978-1", member1)  # member1 checks out
    library.reserve("978-1", member2)  # member2 reserves
    # After return, member2 should be notified
    library.return_copy("978-1/1", member1)
    assert library.get_copy_status("978-1/1") == "reserved"  # Status should be reserved for member2

def test_reserve_duplicate():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member = Member("member1")
    library.register_member(member)  # Register member
    library.add_copy("978-1")
    library.reserve("978-1", member)  # First reservation
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.reserve("978-1", member)  # Attempt to reserve again
    assert "already has a reservation" in str(excinfo.value)

def test_cancel_reservation():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)  # Register members
    library.register_member(member2)
    library.add_copy("978-1")
    library.checkout("978-1", member1)  # member1 checks out
    library.reserve("978-1", member2)  # member2 reserves
    with pytest.raises(Exception) as excinfo:  # General exception since type is unspecified
        library.cancel_reservation("978-1", member1)  # member1 tries to cancel member2's reservation
    assert "no reservation for 978-1" in str(excinfo.value)

def test_member_cancels_own_reservation():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member = Member("member1")
    library.register_member(member)  # Register member
    library.add_copy("978-1")
    library.reserve("978-1", member)  # member reserves
    library.cancel_reservation("978-1", member)  # member cancels own reservation
    library.reserve("978-1", member)  # member can reserve again now
    assert library.get_copy_status("978-1/1") == "reserved"  # New reservation should be granted