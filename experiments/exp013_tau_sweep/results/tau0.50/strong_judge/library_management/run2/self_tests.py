# test_library_circulation.py

import pytest
from solution import Library, Member

def test_add_new_copy_available():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    assert library.get_copy_status(copy_id) == "available"  # AC-1.1

def test_multiple_copies_tracking():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.available_count("978-1") == 2  # AC-1.2

def test_catalogue_record():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    # Assuming a method to retrieve all fields together
    catalogue_record = library.get_catalogue("978-1")
    assert catalogue_record == {
        "isbn": "978-1",
        "title": "Title 1",
        "category": "Fiction",
        "shelf_location": "Shelf A"
    }  # AC-1.3

def test_copy_identifier_combination():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id_1 = library.add_copy("978-1")
    copy_id_2 = library.add_copy("978-1")
    assert copy_id_1 == "978-1/1"  # AC-1.4
    assert copy_id_2 == "978-1/2"

def test_unknown_copy_identifier():
    library = Library()
    result = library.get_copy_status("unknown-id")  # Should handle unknown copy gracefully
    assert result == "unknown-id"  # AC-1.5

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    library.remove_copy(copy_id)
    assert library.available_count("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    result = library.remove_copy(copy_id)  # Should handle removal attempt
    assert result == "not available for removal"  # AC-1.7

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)  # Registering the member
    due_date = library.checkout("978-1", member)
    assert library.get_copy_status(copy_id) == "checked_out"  # AC-2.3
    assert due_date == library.get_checkout_day() + 14  # AC-2.1, assuming 14 days loan period

def test_checkout_no_free_copies():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    member = Member("member-1")
    library.register_member(member)  # Registering the member
    copy_id = library.add_copy("978-1")
    library.checkout("978-1", member)
    result = library.checkout("978-1", Member("member-2"))  # Attempt another checkout
    assert result == "No copies of 978-1 are available"  # AC-2.5

def test_checkout_unknown_book():
    library = Library()
    member = Member("member-1")
    library.register_member(member)  # Registering the member
    result = library.checkout("unknown-isbn", member)  # Checkout unknown book
    assert result == "unknown-isbn"  # AC-2.6

def test_checkout_unknown_member():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    result = library.checkout("978-1", Member("unknown-member"))  # Attempt checkout with unknown member
    assert result == "unknown-member"  # AC-2.7

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)  # Registering the member
    library.checkout("978-1", member)
    assert library.return_copy(copy_id, member) == 0  # AC-3.1

def test_return_late():
    library = Library(fine_per_day=0.50)
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)  # Registering the member
    library.checkout("978-1", member)
    library.set_date("2023-10-04")  # Simulate current date
    # Setting checkout date to 3 days before return
    library.set_checkout_date(copy_id, "2023-09-30")  # Check out on 30th
    assert library.return_copy(copy_id, member) == 1.50  # 3 days late at 0.50 per day (3*0.50=1.50) # AC-3.2

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    result = library.return_copy(copy_id, Member("member-1"))  # Attempt to return not checked out
    assert result == "not checked out"  # AC-3.4

def test_reserve_title():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)  # Member 2 reserves the title
    assert library.get_reservation_status(member2, "978-1") == "queued"  # Should be queued initially

    library.return_copy(copy_id, member1)  # Simulate return
    assert library.get_copy_status(copy_id) == "reserved"  # AC-4.1

def test_reserve_already_reserved_title():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)
    library.checkout("978-1", member)
    library.reserve("978-1", Member("member-2"))
    
    result = library.reserve("978-1", member)  # Same member tries to reserve again
    assert result == "already has a reservation"  # AC-4.6

def test_cancel_reservation():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)

    library.cancel_reservation("978-1", member2)  # Member 2 cancels their reservation
    assert not library.has_reservation(member2, "978-1")  # AC-5.1
    
    # Return the copy to see if it goes back to the shelf
    library.return_copy(copy_id, member1)
    assert library.get_copy_status(copy_id) == "available"  # Should be available now

def test_cancel_reservation_no_reservation():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    member1 = Member("member-1")
    library.register_member(member1)
    result = library.cancel_reservation("978-1", member1)  # No reservation to cancel
    assert result == "has no reservation for that ISBN"  # AC-5.3

def test_cancel_other_member_reservation():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)

    result = library.cancel_reservation("978-1", member1)  # Member 1 tries to cancel member 2's reservation
    assert result == "cannot cancel another member's reservation"  # AC-5.4

def test_lapse_hold():
    library = Library(hold_period=3)
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)
    library.reserve("978-1", member)  # Member reserves the title

    # Simulate the hold period expiration
    library.set_date("2023-10-01")  # Grant hold on this date
    library.set_date("2023-10-03")  # Last day of hold
    assert library.get_copy_status(copy_id) == "reserved"  # Still reserved on last day
    library.set_date("2023-10-04")  # Day after hold expires
    assert library.get_copy_status(copy_id) == "available"  # Should now be available  # AC-5.5

def test_expiry_transfers_to_next_reserver():
    library = Library(hold_period=3)
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.register_member(member1)
    library.register_member(member2)
    library.reserve("978-1", member1)
    library.reserve("978-1", member2)  # Second member reserves

    # Simulate the hold period expiration
    library.set_date("2023-10-01")  # Grant hold on this date
    library.set_date("2023-10-03")  # Last day of hold
    library.set_date("2023-10-04")  # Day after hold expires
    assert library.get_copy_status(copy_id) == "reserved"  # Should be reserved for member 2 now

def test_checkout_with_multiple_copies_checked_out():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id_1 = library.add_copy("978-1")
    copy_id_2 = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)
    library.checkout("978-1", member)  # Checkout first copy
    library.checkout("978-1", member)  # Checkout second copy
    assert library.get_copy_status(copy_id_1) == "checked_out"  # First copy checked out
    assert library.get_copy_status(copy_id_2) == "checked_out"  # Second copy also checked out

def test_return_available_copy_diff_member():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.return_copy(copy_id, member1)  # Return by member 1
    assert library.get_copy_status(copy_id) == "available"  # Should be available now
    library.checkout("978-1", member2)  # Member 2 checks out the now available copy
    assert library.get_copy_status(copy_id) == "checked_out"  # Should now be checked out

def test_holding_copy_for_reserver_only():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)
    library.return_copy(copy_id, member1)  # Return the copy
    assert library.get_copy_status(copy_id) == "reserved"  # Should be reserved for member 2
    result = library.checkout("978-1", Member("some-other-member"))  # Try to checkout for another member
    assert result == "No copies of 978-1 are available"  # Must not be allowed to checkout

def test_reserving_copy_when_available():
    library = Library()
    library.add_title("978-1", "Title 1", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.register_member(member)
    library.reserve("978-1", member)  # Should reserve the available copy directly
    assert library.get_copy_status(copy_id) == "reserved"  # Copy should now be reserved
    assert library.available_count("978-1") == 0  # No available copies should exist now