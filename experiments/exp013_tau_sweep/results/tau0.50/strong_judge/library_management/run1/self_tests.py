import pytest
from solution import Library, Member

def test_add_new_copy_is_available():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    assert library.get_copy_status(copy_id) == "available"  # AC-1.1

def test_multiple_copies_tracking():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_copies("978-1") == 2  # AC-1.2

def test_catalogue_record():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    title_info = library.get_title_info("978-1")
    assert title_info["isbn"] == "978-1"  # AC-1.3
    assert title_info["title"] == "Test Title"  # AC-1.3
    assert title_info["category"] == "Fiction"  # AC-1.3
    assert title_info["shelf_location"] == "A1"  # AC-1.3

def test_copy_identifier_format():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id1 = library.add_copy("978-1")
    copy_id2 = library.add_copy("978-1")
    assert copy_id1 == "978-1/1"  # AC-1.4
    assert copy_id2 == "978-1/2"  # AC-1.4

def test_status_of_unknown_copy_identifier():
    library = Library()
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.get_copy_status("unknown_id")
    assert "unknown_id" in str(excinfo.value)  # AC-1.5

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    library.remove_copy(copy_id)
    assert library.get_available_copies("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.remove_copy(copy_id)
    assert "not available for removal" in str(excinfo.value)  # AC-1.7

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    assert library.get_copy_status(copy_id) == "checked_out"  # AC-2.3

def test_checkout_updates_due_date():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    # Due date should be current date + 14 days
    # Assuming we have a method get_due_date that calculates this
    assert library.get_due_date(copy_id) == library.get_current_date() + 14  # AC-2.1, AC-2.2

def test_checkout_no_available_copies():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member1")
    library.register_member(member)
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.checkout("978-1", member)
    assert "No copies of 978-1 are available" in str(excinfo.value)  # AC-2.5

def test_checkout_unknown_isbn():
    library = Library()
    member = Member("member1")
    library.register_member(member)
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.checkout("unknown_isbn", member)
    assert "unknown_isbn" in str(excinfo.value)  # AC-2.6

def test_checkout_unregistered_member():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    unregistered_member = Member("unregistered_member")
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.checkout("978-1", unregistered_member)
    assert "unregistered_member" in str(excinfo.value)  # AC-2.7

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    library.return_copy(copy_id, member)
    assert library.get_copy_status(copy_id) == "available"  # AC-3.3

def test_return_late_fine():
    library = Library(fine_rate=0.5)
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.checkout("978-1", member)
    # Simulate returning the copy 3 days late
    library.set_current_date(library.get_current_date() + 4)  # Assuming we can set the current date
    fine = library.return_copy(copy_id, member)  # Assume this returns the fine amount
    assert fine == 1.5  # AC-3.2

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.return_copy(copy_id, Member("member1"))
    assert "not checked out" in str(excinfo.value)  # AC-3.4

def test_reserve_title():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member = Member("member1")
    library.register_member(member)
    library.reserve("978-1", member)
    assert library.get_copy_status(copy_id) == "reserved"  # AC-4.1

def test_reserve_when_unavailable():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)
    # Assuming the implementation allows us to check the reservation status
    assert library.get_reservation_status("978-1", member2) == "queued"  # AC-4.1

def test_checkout_reserved_copy():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    copy_id = library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)
    library.register_member(member2)
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)
    library.return_copy(copy_id, member1)
    library.checkout("978-1", member2)  # Assuming this checks out the reserved copy
    assert library.get_copy_status(copy_id) == "checked_out"  # AC-4.3

def test_cancel_reservation():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member1")
    library.register_member(member)
    library.reserve("978-1", member)
    library.cancel_reservation("978-1", member)
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.2

def test_cancel_reservation_not_owned():
    library = Library()
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.register_member(member1)
    library.reserve("978-1", member1)
    with pytest.raises(Exception) as excinfo:  # Use unspecified error type
        library.cancel_reservation("978-1", member2)
    assert "no reservation for this ISBN" in str(excinfo.value)  # AC-5.3

def test_lapse_hold():
    library = Library(hold_period=3)
    library.add_title("978-1", "Test Title", "Fiction", "A1")
    member = Member("member1")
    library.register_member(member)
    library.reserve("978-1", member)
    # Simulate the hold period lapse
    library.set_current_date(library.get_current_date() + 4)  # Assuming we can set the current date
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.5