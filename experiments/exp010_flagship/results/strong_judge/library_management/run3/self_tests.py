# test_library_circulation.py

import pytest
from solution import Library, Member, Copy, Title

# US-1: Catalogue and inventory

def test_add_new_copy_is_available():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    assert library.get_copy_status("978-1/1") == "available"  # Newly added copy should be available

def test_multiple_copies_count():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_count("978-1") == 2  # Two copies should be available

def test_catalogue_records_details():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    details = library.get_title_details("978-1")
    assert details[0] == "978-1"  # Check ISBN
    assert details[1] == "Book Title"  # Check title
    assert details[2] == "Fiction"  # Check category
    assert details[3] == "A1"  # Check shelf location

def test_copy_identifier_format():
    assert Copy("978-1", 1).identifier() == "978-1/1"  # First copy
    assert Copy("978-1", 2).identifier() == "978-1/2"  # Second copy

def test_status_of_unknown_copy_identifier():
    library = Library()
    with pytest.raises(ValueError, match="unknown-identifier"):
        library.get_copy_status("unknown-identifier")

def test_remove_available_copy():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    library.remove_copy("978-1/1")
    assert library.get_available_count("978-1") == 0  # Count should be zero after removal

def test_remove_checked_out_copy():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member(name="John Doe")
    library.register_member(member)
    library.checkout("978-1", member)
    with pytest.raises(ValueError, match="not available for removal"):
        library.remove_copy("978-1/1")

# US-2: Checkout

def test_checkout_available_copy():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member(name="John Doe")
    library.register_member(member)
    due_date = library.checkout("978-1", member)
    assert due_date == library.current_date + 14  # Due date should be 14 days later

def test_checkout_no_free_copies():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member(name="John Doe")
    library.register_member(member)
    library.checkout("978-1", member)  # Checkout first copy
    with pytest.raises(ValueError, match="No copies of 978-1 are available"):
        library.checkout("978-1", member)  # Attempt to checkout again

def test_checkout_unknown_isbn():
    library = Library()
    member = Member(name="John Doe")
    library.register_member(member)
    with pytest.raises(ValueError, match="unknown-isbn"):
        library.checkout("unknown-isbn", member)

def test_checkout_unregistered_member():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member(name="Unknown Member")  # Unregistered member
    with pytest.raises(ValueError, match="unknown-member"):
        library.checkout("978-1", member)

# US-3: Returns and fines

def test_return_on_time():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member(name="John Doe")
    library.register_member(member)
    library.checkout("978-1", member)
    fine = library.return_copy("978-1/1")  # On time
    assert fine == 0  # No fine for on-time returns

def test_return_late():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member(name="John Doe")
    library.register_member(member)
    library.checkout("978-1", member)
    library.set_fine_rate(0.50)  # Configure fine rate
    library.current_date += 3  # Simulate 3 days pass
    fine = library.return_copy("978-1/1")  # 3 days late
    assert fine == 1.50  # Fine should be 3 days * 0.50 per day

def test_return_not_checked_out():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    library.add_copy("978-1")
    with pytest.raises(ValueError, match="not checked out"):
        library.return_copy("978-1/1")

# US-4: Reservations and holds

def test_reserve_unavailable_title():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    member = Member(name="John Doe")
    library.register_member(member)
    library.add_copy("978-1")
    library.checkout("978-1", member)
    library.reserve("978-1", member)  # Member reserves the title

    # Simulate return of the copy
    library.return_copy("978-1/1")
    assert library.get_copy_status("978-1/1") == "reserved"  # Copy should be reserved for the member

def test_reserve_already_reserved_title():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    member = Member(name="John Doe")
    library.register_member(member)
    library.add_copy("978-1")
    library.checkout("978-1", member)
    library.reserve("978-1", member)  # Member reserves the title
    with pytest.raises(ValueError, match="already has a reservation"):
        library.reserve("978-1", member)  # Member tries to reserve the same title again

def test_reserve_different_member():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    member1 = Member(name="John Doe")
    member2 = Member(name="Jane Doe")
    library.register_member(member1)
    library.register_member(member2)
    library.add_copy("978-1")
    library.checkout("978-1", member1)
    library.reserve("978-1", member1)  # Member 1 reserves the title
    library.return_copy("978-1/1")  # Return the copy
    library.reserve("978-1", member2)  # Member 2 reserves the same title
    assert library.get_copy_status("978-1/1") == "reserved"  # Copy should be reserved for member 2

# US-5: Cancellations and hold expiry

def test_cancel_queued_reservation():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    member = Member(name="John Doe")
    library.register_member(member)
    library.add_copy("978-1")
    library.reserve("978-1", member)  # Member reserves the title
    library.cancel_reservation("978-1", member)  # Cancel reservation
    assert library.get_copy_status("978-1/1") == "available"  # Copy should be available again

def test_cancel_non_existent_reservation():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    member = Member(name="John Doe")
    library.register_member(member)
    with pytest.raises(ValueError, match="has no reservation for"):
        library.cancel_reservation("978-1", member)  # Cancel non-existent reservation

def test_hold_expiry():
    library = Library()
    title = Title(isbn="978-1", title="Book Title", category="Fiction", shelf_location="A1")
    library.add_title(title)
    member = Member(name="John Doe")
    library.register_member(member)
    library.add_copy("978-1")
    library.reserve("978-1", member)  # Member reserves the title
    library.set_hold_period(3)  # Set hold period to 3 days
    library.current_date += 3  # Simulate 3 days pass
    library.expire_holds()  # Expire holds
    assert library.get_copy_status("978-1/1") == "available"  # Copy should be available again