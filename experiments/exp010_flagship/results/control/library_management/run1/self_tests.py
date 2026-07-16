from solution import Library, Member, ReservationError, UnknownBookError, UnknownMemberError, DuplicateReservationError

def test_add_new_copy_makes_it_available():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    assert library.get_copy_status("978-1/1") == "available"  # Newly added copy should be available

def test_multiple_copies_are_tracked_individually():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_available_count("978-1") == 2  # Should reflect two available copies

def test_catalogue_records_title_details():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    assert library.get_title_details("978-1") == ("978-1", "Title One", "Fiction", "Shelf A")

def test_copy_identifier_format():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_copy_identifier("978-1", 1) == "978-1/1"  # First copy identifier
    assert library.get_copy_identifier("978-1", 2) == "978-1/2"  # Second copy identifier

def test_status_of_unknown_copy_identifier():
    library = Library()
    with pytest.raises(ValueError, match="Unknown copy identifier: unknown-id"):
        library.get_copy_status("unknown-id")  # Should raise an error for unknown copy identifier

def test_remove_available_copy_decreases_count():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    library.remove_copy("978-1/1")
    assert library.get_available_count("978-1") == 0  # Should reflect zero available copies after removal

def test_remove_checked_out_copy_fails():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    with pytest.raises(ValueError, match="Copy 978-1/1 not available for removal"):
        library.remove_copy("978-1/1")  # Should raise an error since the copy is checked out

def test_checkout_lends_available_copy():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member-1")
    library.checkout("978-1", member)
    assert library.get_copy_status("978-1/1") == "checked_out"  # Should be marked as checked out
    assert library.get_due_date("978-1", member) == library.get_checkout_date() + timedelta(days=14)  # Due date should be set

def test_checkout_no_free_copies():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member = Member("member-1")
    library.add_copy("978-1")
    library.checkout("978-1", member)
    with pytest.raises(ValueError, match="No copies of 978-1 are available"):
        library.checkout("978-1", Member("member-2"))  # Should raise an error for no available copies

def test_checkout_unknown_book():
    library = Library()
    member = Member("member-1")
    with pytest.raises(UnknownBookError, match="Unknown book: 978-1"):
        library.checkout("978-1", member)  # Should raise an error for unknown book

def test_checkout_unknown_member():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    with pytest.raises(UnknownMemberError, match="Unknown member: unknown-member"):
        library.checkout("978-1", Member("unknown-member"))  # Should raise an error for unknown member

def test_return_on_time_costs_nothing():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member = Member("member-1")
    library.add_copy("978-1")
    library.checkout("978-1", member)
    library.return_copy("978-1/1", member)
    assert library.get_fine(member) == 0  # Should be zero if returned on time

def test_late_return_calculates_fine():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member = Member("member-1")
    library.add_copy("978-1")
    library.checkout("978-1", member)
    
    # Simulate late return (e.g., 3 days late)
    library.set_current_date(library.get_checkout_date() + timedelta(days=17))  # 3 days late
    library.return_copy("978-1/1", member)
    assert library.get_fine(member) == 1.5  # Fine should be 3 days * 0.50 per day

def test_return_not_checked_out_fails():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    with pytest.raises(ValueError, match="Copy 978-1/1 is not checked out"):
        library.return_copy("978-1/1", Member("member-1"))  # Should raise an error for not checked out

def test_reserve_title_and_notify_when_returned():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.checkout("978-1", member1)  # member-1 checks it out
    library.reserve("978-1", member2)  # member-2 reserves it

    library.return_copy("978-1/1", member1)  # member-1 returns it
    assert library.get_copy_status("978-1/1") == "reserved"  # It should be reserved for member-2

def test_hold_on_returned_copy():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.checkout("978-1", member1)  # member-1 checks it out
    library.reserve("978-1", member2)  # member-2 reserves it

    library.return_copy("978-1/1", member1)  # member-1 returns it
    assert library.get_reserving_member("978-1/1") == member2  # member-2 should be notified

def test_reserve_same_title_twice_fails():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member-1")
    library.reserve("978-1", member)  # First reservation
    with pytest.raises(DuplicateReservationError, match="member-1 already has a reservation"):
        library.reserve("978-1", member)  # Should fail since member cannot reserve twice

def test_lapsed_hold_period():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member-1")
    library.reserve("978-1", member)
    
    # Simulate the lapse of hold period
    library.set_current_date(library.get_current_date() + timedelta(days=4))  # Assuming default hold period is 3 days
    assert library.get_copy_status("978-1/1") == "available"  # Should reflect that the copy is available again

def test_cancelled_queued_reservation_notified():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.reserve("978-1", member1)  # member-1 reserves
    library.reserve("978-1", member2)  # member-2 reserves

    library.cancel_reservation("978-1", member1)  # member-1 cancels reservation
    assert library.get_copy_status("978-1/1") == "available"  # Should be available again, member-2 should not be notified

def test_cancel_reservation_fails_if_not_reserved():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member = Member("member-1")
    with pytest.raises(ValueError, match="member-1 has no reservation for 978-1"):
        library.cancel_reservation("978-1", member)  # Should raise error as member has no reservation

def test_cancel_reservation_for_other_member_fails():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.reserve("978-1", member1)  # member-1 reserves
    with pytest.raises(ValueError, match="Cannot cancel reservation for another member"):
        library.cancel_reservation("978-1", member2)  # Should raise error as member2 cannot cancel member1's reservation

def test_holds_expire_and_next_member_is_notified():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member1 = Member("member-1")
    member2 = Member("member-2")
    library.reserve("978-1", member1)  # member-1 reserves
    library.reserve("978-1", member2)  # member-2 reserves

    # Simulate lapse of hold period for member-1
    library.set_current_date(library.get_current_date() + timedelta(days=4))  # Assuming default hold period is 3 days
    assert library.get_copy_status("978-1/1") == "reserved"  # Should be reserved for member-2 now

def test_uncollected_hold_lapses():
    library = Library()
    library.add_title("978-1", "Title One", "Fiction", "Shelf A")
    library.add_copy("978-1")
    member = Member("member-1")
    library.reserve("978-1", member)  # member-1 reserves
    
    # Simulate lapse of hold period
    library.set_current_date(library.get_current_date() + timedelta(days=4))  # Assuming default hold period is 3 days
    assert library.get_copy_status("978-1/1") == "available"  # Should be available again after lapse