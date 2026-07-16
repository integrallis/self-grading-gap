import pytest
from solution import Library, Member, Title

def test_add_new_copy_increases_available_count():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    assert library.available_count("978-1") == 1  # 1 new copy added

def test_multiple_copies_track_individually():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.available_count("978-1") == 2  # 2 copies added

def test_title_catalogue_records_details():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    # Assuming get_title_details returns the tuple (ISBN, title, category, shelf_location)
    details = library.get_title_details("978-1")
    assert details[0] == "978-1" and details[1] == "Test Title" and details[2] == "Fiction" and details[3] == "A1"

def test_copy_identifier_format():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_copy_identifier("978-1", 1) == "978-1/1"  # first copy
    assert library.get_copy_identifier("978-1", 2) == "978-1/2"  # second copy

def test_unknown_copy_identifier_error():
    library = Library()
    with pytest.raises(Exception) as excinfo:
        library.get_copy_status("978-1/1")
    assert "Unknown copy identifier: 978-1/1" in str(excinfo.value)  # error message matches

def test_remove_available_copy_decreases_count():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    library.remove_copy("978-1/1")
    assert library.available_count("978-1") == 0  # count decremented

def test_remove_checked_out_copy_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:
        library.remove_copy("978-1/1")
    assert "not available for removal" in str(excinfo.value)  # error message matches

def test_checkout_available_copy():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout("978-1", member)
    assert library.get_copy_status("978-1/1") == "checked_out"  # status updates

def test_checkout_no_free_copies_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member = Member("member1")
    with pytest.raises(Exception) as excinfo:
        library.checkout("978-1", member)
    assert "No copies of 978-1 are available" in str(excinfo.value)  # error message matches

def test_checkout_unknown_isbn_error():
    library = Library()
    member = Member("member1")
    with pytest.raises(Exception) as excinfo:
        library.checkout("978-2", member)
    assert "Unknown book: 978-2" in str(excinfo.value)  # error message matches

def test_checkout_unregistered_member_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:
        library.checkout("978-1", Member("unregistered_member"))  # a simulated unregistered member
    assert "Unknown member: unregistered_member" in str(excinfo.value)  # error message matches

def test_return_on_time_no_fine():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout("978-1", member)
    library.return_copy("978-1/1", member)
    assert library.get_fine(member) == 0  # no fine for on-time return

def test_return_late_fine_calculation():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout("978-1", member)
    # Simulating late return
    library.return_copy("978-1/1", member, days_late=3)  # Assume this method calculates fine
    assert library.get_fine(member) == 1.50  # 3 days late at 0.50 per day

def test_return_not_checked_out_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:
        library.return_copy("978-1/1", Member("member1"))  # member who did not check out
    assert "not checked out" in str(excinfo.value)  # error message matches

def test_reserve_title_when_unavailable():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member1 = Member("member1")
    member2 = Member("member2")
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)
    assert library.get_copy_status("978-1/1") == "reserved"  # member2 should be notified and copy reserved

def test_next_reserved_member_notified_on_return():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member1 = Member("member1")
    member2 = Member("member2")
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)
    library.return_copy("978-1/1", member1)
    assert library.get_copy_status("978-1/1") == "reserved"  # member2 should be notified and copy reserved

def test_cancel_queued_reservation():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member = Member("member1")
    library.reserve("978-1", member)
    library.cancel_reservation("978-1", member)
    assert library.get_reservation_status("978-1", member) is None  # reservation should be cancelled

def test_cancel_reservation_after_hold():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member1 = Member("member1")
    member2 = Member("member2")
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)
    library.return_copy("978-1/1", member1)  # member1 returns the book
    assert library.get_copy_status("978-1/1") == "reserved"  # member2's hold should be granted
    library.cancel_reservation("978-1", member2)  # canceling the reservation
    assert library.get_copy_status("978-1/1") == "available"  # copy should be available again

def test_cancel_nonexistent_reservation_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member = Member("member1")
    with pytest.raises(Exception) as excinfo:
        library.cancel_reservation("978-1", member)
    assert "No reservation for 978-1" in str(excinfo.value)  # error message matches

def test_cancel_others_hold_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member1 = Member("member1")
    member2 = Member("member2")
    library.reserve("978-1", member1)
    with pytest.raises(Exception) as excinfo:
        library.cancel_reservation("978-1", member2)  # member2 cannot cancel member1's reservation
    assert "No reservation for 978-1" in str(excinfo.value)  # error message matches

def test_uncollected_hold_lapses():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member = Member("member1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    # Simulating time passing for the hold to lapse
    library.lapse_hold("978-1")  # Assume this method checks and simulates the lapse
    assert library.get_copy_status("978-1/1") == "available"  # copy should be available again after lapse

def test_hold_lapse_notifies_next_reserver():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member1 = Member("member1")
    member2 = Member("member2")
    library.add_copy("978-1")
    library.reserve("978-1", member1)
    library.reserve("978-1", member2)
    # Simulating time passing for the hold to lapse
    library.lapse_hold("978-1")  # Assume this method checks and simulates the lapse
    assert library.get_copy_status("978-1/1") == "reserved"  # member2 should be notified and copy reserved

def test_reserving_while_copy_available():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.reserve("978-1", member)  # member reserves while copy is available
    assert library.get_copy_status("978-1/1") == "reserved"  # member1 should now have the copy reserved

def test_duplicate_reservation_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member = Member("member1")
    library.reserve("978-1", member)
    with pytest.raises(Exception) as excinfo:
        library.reserve("978-1", member)  # member tries to reserve again
    assert "already has a reservation" in str(excinfo.value)  # error message matches

def test_second_member_reservation():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.reserve("978-1", member1)  # member1 reserves
    library.checkout("978-1", member1)  # member1 checks out
    library.reserve("978-1", member2)  # member2 reserves while member1 has the copy checked out
    assert library.get_copy_status("978-1/1") == "reserved"  # member2's reservation should be valid

def test_each_member_collects_specific_copy():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.reserve("978-1", member1)
    library.reserve("978-1", member2)
    library.return_copy("978-1/1", member1)  # member1 returns their copy
    assert library.get_copy_status("978-1/1") == "reserved"  # member1's copy should be reserved for them
    library.checkout("978-1", member1)  # member1 collects their reserved copy
    assert library.get_copy_status("978-1/1") == "checked_out"  # should now be checked out

def test_cancelled_reservation_skipped_on_return():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    library.add_copy("978-1")
    member1 = Member("member1")
    member2 = Member("member2")
    library.reserve("978-1", member1)  # member1 reserves
    library.reserve("978-1", member2)  # member2 reserves
    library.cancel_reservation("978-1", member1)  # member1 cancels their reservation
    library.return_copy("978-1/1", member1)  # member1 returns the copy
    assert library.get_copy_status("978-1/1") == "available"  # copy should be available again after lapse

def test_cancel_others_hold_error():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member1 = Member("member1")
    member2 = Member("member2")
    library.reserve("978-1", member1)
    library.reserve("978-1", member2)
    with pytest.raises(Exception) as excinfo:
        library.cancel_reservation("978-1", member2)  # member2 cannot cancel member1's reservation
    assert "No reservation for 978-1" in str(excinfo.value)  # error message matches

def test_default_hold_period():
    library = Library()
    title = Title("978-1", "Test Title", "Fiction", "A1")
    library.add_title(title)
    member = Member("member1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    # Simulating time passing for the hold to lapse
    library.lapse_hold("978-1")  # Assume this method checks and simulates the lapse
    assert library.get_copy_status("978-1/1") == "available"  # copy should be available again after lapse