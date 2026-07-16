from solution import Library, Member, Copy, Reservation

def test_add_new_copy_available():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    assert library.get_copy_status(copy_id) == "available"  # AC-1.1

def test_add_multiple_copies_track_individually():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id1 = library.add_copy("978-1")
    copy_id2 = library.add_copy("978-1")
    assert library.get_available_count("978-1") == 2  # AC-1.2
    assert library.get_copy_status(copy_id1) == "available"
    assert library.get_copy_status(copy_id2) == "available"

def test_catalogue_records_title_details():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    title_info = library.get_title_info("978-1")
    assert title_info == ("978-1", "Sample Title", "Fiction", "Shelf A")  # AC-1.3

def test_copy_identifier_format():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id1 = library.add_copy("978-1")
    copy_id2 = library.add_copy("978-1")
    assert copy_id1 == "978-1/1"  # AC-1.4
    assert copy_id2 == "978-1/2"

def test_status_of_unknown_copy_identifier():
    library = Library()
    with pytest.raises(ValueError) as e:
        library.get_copy_status("unknown-id")
    assert str(e.value) == "Unknown copy identifier: unknown-id"  # AC-1.5

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    library.remove_copy(copy_id)
    assert library.get_available_count("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout(copy_id, member)
    with pytest.raises(ValueError) as e:
        library.remove_copy(copy_id)
    assert str(e.value) == "Copy is not available for removal."  # AC-1.7

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    due_date = library.checkout(copy_id, member)
    assert due_date is not None  # AC-2.1
    assert library.get_copy_status(copy_id) == "checked_out"  # AC-2.3

def test_checkout_no_free_copies():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout(copy_id, member)
    with pytest.raises(ValueError) as e:
        library.checkout(copy_id, Member("member-2"))
    assert str(e.value) == "No copies of 978-1 are available."  # AC-2.5

def test_checkout_unknown_book():
    library = Library()
    member = Member("member-1")
    with pytest.raises(ValueError) as e:
        library.checkout("978-1", member)
    assert str(e.value) == "Unknown book: 978-1"  # AC-2.6

def test_checkout_unregistered_member():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    with pytest.raises(ValueError) as e:
        library.checkout(copy_id, Member("unknown-member"))
    assert str(e.value) == "Unknown member: unknown-member"  # AC-2.7

def test_return_on_or_before_due_date():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout(copy_id, member)
    assert library.return_copy(copy_id, member, due_date="2023-10-01") == 0.0  # AC-3.1

def test_return_late_fine():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout(copy_id, member)
    assert library.return_copy(copy_id, member, due_date="2023-09-28") == 1.5  # AC-3.2 (3 days late)

def test_return_available_again():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    member = Member("member-1")
    library.checkout(copy_id, member)
    library.return_copy(copy_id, member, due_date="2023-10-01")
    assert library.get_copy_status(copy_id) == "available"  # AC-3.3

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    copy_id = library.add_copy("978-1")
    with pytest.raises(ValueError) as e:
        library.return_copy(copy_id, Member("member-2"), due_date="2023-10-01")
    assert str(e.value) == "Copy is not checked out."  # AC-3.4

def test_reserve_title():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.add_copy("978-1")  # make copy available
    library.checkout("978-1/1", member1)  # member 1 checks out the only copy
    library.reserve("978-1", member2)  # member 2 reserves it, should be notified when returned
    assert library.get_reservation_status(member2, "978-1") == "reserved"  # AC-4.1

def test_reserve_when_copy_available():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member1 = Member("member-1")
    member2 = Member("member-2")
    copy_id = library.add_copy("978-1")
    library.reserve("978-1", member1)  # member 1 reserves it
    assert library.get_copy_status(copy_id) == "reserved"  # AC-4.5

def test_duplicate_reservation():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = Member("member-1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    with pytest.raises(ValueError) as e:
        library.reserve("978-1", member)  # member tries to reserve again
    assert str(e.value) == "Member already has a reservation."  # AC-4.6

def test_cancellations():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = Member("member-1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    library.cancel_reservation("978-1", member)
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.1

def test_cancel_reservation_not_found():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member = Member("member-1")
    with pytest.raises(ValueError) as e:
        library.cancel_reservation("978-1", member)  # member does not have reservation
    assert str(e.value) == "Member has no reservation for this ISBN."  # AC-5.3

def test_cancel_granted_hold():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.add_copy("978-1")
    library.reserve("978-1", member1)
    library.checkout("978-1/1", member1)  # member 1 checks out
    library.reserve("978-1", member2)  # member 2 reserves
    library.cancel_reservation("978-1", member1)  # member 1 cancels
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.2

def test_lapse_hold():
    library = Library()
    library.add_title("978-1", "Sample Title", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member-1")
    library.reserve("978-1", member)
    library.lapse_hold("978-1")  # lapse the hold
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.5