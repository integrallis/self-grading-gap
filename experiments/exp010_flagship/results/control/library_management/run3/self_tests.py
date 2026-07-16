from solution import Library, Member, Copy, Title  # assuming these are the classes to be implemented

def test_add_new_copy_is_available():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    assert library.get_copy_status("978-1/1") == "available"  # AC-1.1

def test_multiple_copies_tracking():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_copies_count("978-1") == 2  # AC-1.2

def test_title_details_retrieval():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    assert library.get_title_details("978-1") == ("978-1", "Test Title", "Fiction", "Shelf A")  # AC-1.3

def test_copy_identifier_format():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    assert library.get_copy_identifier("978-1", 1) == "978-1/1"  # AC-1.4
    assert library.get_copy_identifier("978-1", 2) == "978-1/2"  # AC-1.4

def test_unknown_copy_identifier():
    library = Library()
    with pytest.raises(ValueError) as excinfo:
        library.get_copy_status("unknown-copy")
    assert str(excinfo.value) == "Unknown copy identifier: unknown-copy"  # AC-1.5

def test_remove_available_copy():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    library.remove_copy("978-1/1")
    assert library.get_available_copies_count("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout_copy("member1", "978-1")
    with pytest.raises(ValueError) as excinfo:
        library.remove_copy("978-1/1")
    assert str(excinfo.value) == "Copy '978-1/1' not available for removal"  # AC-1.7

def test_checkout_available_copy():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    due_date = library.checkout_copy("member1", "978-1")
    assert library.get_copy_status("978-1/1") == "checked_out"  # AC-2.3
    assert due_date is not None  # AC-2.1

def test_checkout_no_free_copies():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout_copy("member1", "978-1")
    with pytest.raises(ValueError) as excinfo:
        library.checkout_copy("member2", "978-1")
    assert str(excinfo.value) == "No copies of 978-1 are available"  # AC-2.5

def test_checkout_unknown_isbn():
    library = Library()
    with pytest.raises(ValueError) as excinfo:
        library.checkout_copy("member1", "unknown-isbn")
    assert str(excinfo.value) == "Unknown book: unknown-isbn"  # AC-2.6

def test_checkout_unregistered_member():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    with pytest.raises(ValueError) as excinfo:
        library.checkout_copy("unknown-member", "978-1")
    assert str(excinfo.value) == "Unknown member: unknown-member"  # AC-2.7

def test_return_on_time():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout_copy("member1", "978-1")
    library.return_copy("978-1/1", member)
    assert library.get_copy_status("978-1/1") == "available"  # AC-3.3

def test_return_late():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout_copy("member1", "978-1")
    library.set_due_date("978-1/1", -3)  # Simulate being 3 days late
    fine = library.return_copy("978-1/1", member)
    assert fine == 1.50  # AC-3.2

def test_return_not_checked_out():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    with pytest.raises(ValueError) as excinfo:
        library.return_copy("978-1/1", Member("member1"))
    assert str(excinfo.value) == "Copy '978-1/1' is not checked out"  # AC-3.4

def test_reserve_title():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout_copy("member1", "978-1")  # member1 checks out the copy
    library.reserve_title("member2", "978-1")
    assert library.get_copy_status("978-1/1") == "reserved"  # AC-4.2

def test_reserve_when_copy_is_available():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.reserve_title("member1", "978-1")
    assert library.get_copy_status("978-1/1") == "reserved"  # AC-4.5

def test_cancel_reservation():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.reserve_title("member1", "978-1")
    library.cancel_reservation("member1", "978-1")
    with pytest.raises(ValueError) as excinfo:
        library.get_copy_status("978-1/1")
    assert str(excinfo.value) == "Copy '978-1/1' is not reserved"  # AC-5.1

def test_cancel_reservation_not_owned():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.reserve_title("member1", "978-1")
    with pytest.raises(ValueError) as excinfo:
        library.cancel_reservation("member2", "978-1")
    assert str(excinfo.value) == "Member does not have a reservation for ISBN: 978-1"  # AC-5.3

def test_expired_hold():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "Shelf A")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.reserve_title(member, "978-1")
    library.set_hold_period(0)  # Simulate expiry
    library.check_expired_holds()
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.5