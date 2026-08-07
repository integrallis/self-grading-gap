import pytest
from solution import Library, Member

def test_add_copy_to_catalogue():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    assert library.get_copy_status("978-1/1") == "available"  # AC-1.1

def test_multiple_copies_tracking():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.available_count("978-1") == 2  # AC-1.2

def test_catalogue_record():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    title_info = library.get_title_info("978-1")  # AC-1.3
    assert title_info[0] == "978-1"
    assert title_info[1] == "Title A"
    assert title_info[2] == "Category A"
    assert title_info[3] == "Shelf A"

def test_copy_identifier_format():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    library.add_copy("978-1")
    assert library.get_copy_status("978-1/1") == "available"  # AC-1.4
    assert library.get_copy_status("978-1/2") == "available"  # AC-1.4

def test_status_of_unknown_copy_identifier():
    library = Library()
    with pytest.raises(Exception) as excinfo:
        library.get_copy_status("unknown_id")  # AC-1.5
    assert "unknown_id" in str(excinfo.value)

def test_remove_available_copy():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    library.remove_copy("978-1/1")
    assert library.available_count("978-1") == 0  # AC-1.6

def test_remove_checked_out_copy():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.checkout("978-1", member)
    with pytest.raises(Exception) as excinfo:
        library.remove_copy("978-1/1")  # AC-1.7
    assert "not available for removal" in str(excinfo.value)

def test_checkout_available_copy():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    checkout_date = "2023-10-01"  # Example checkout date
    library.set_current_date(checkout_date)  # Set the date for the checkout
    library.checkout("978-1", member)  # Checkout the book
    assert library.get_copy_status("978-1/1") == "checked_out"  # AC-2.3

def test_checkout_no_available_copies():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    member1 = Member("member1")
    member2 = Member("member2")
    library.add_copy("978-1")
    library.checkout("978-1", member1)
    with pytest.raises(Exception) as excinfo:
        library.checkout("978-1", member2)  # AC-2.5
    assert "No copies of 978-1 are available" in str(excinfo.value)

def test_checkout_unknown_isbn():
    library = Library()
    member = Member("member1")
    with pytest.raises(Exception) as excinfo:
        library.checkout("978-2", member)  # AC-2.6
    assert "978-2" in str(excinfo.value)

def test_checkout_unregistered_member():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:
        library.checkout("978-1", Member("unknown_member"))  # AC-2.7
    assert "unknown_member" in str(excinfo.value)

def test_return_on_time():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.set_current_date("2023-10-01")  # Checkout date
    library.checkout("978-1", member)
    assert library.return_copy("978-1/1", member, return_date="2023-10-15") == 0  # AC-3.1

def test_return_late():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    member = Member("member1")
    library.set_current_date("2023-10-01")  # Checkout date
    library.checkout("978-1", member)
    library.set_fine_per_day(0.50)  # Assuming a 0.50 fine per day
    assert library.return_copy("978-1/1", member, return_date="2023-10-18") == 1.50  # AC-3.2

def test_return_not_checked_out():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    library.add_copy("978-1")
    with pytest.raises(Exception) as excinfo:
        library.return_copy("978-1/1", Member("member1"))  # AC-3.4
    assert "is not checked out" in str(excinfo.value)

def test_reserve_title_not_available():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    member1 = Member("member1")
    member2 = Member("member2")
    library.add_copy("978-1")
    library.checkout("978-1", member1)
    library.reserve("978-1", member2)  # Member 2 reserves while copy 1 is checked out
    library.return_copy("978-1/1", member1)  # Return the checked-out copy
    assert library.get_copy_status("978-1/1") == "reserved"  # AC-4.1
    # Notification check (just ensuring notification occurs, not checking exact text)
    assert library.has_notification(member2)

def test_reserve_title_with_available_copy():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    member = Member("member1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    assert library.get_copy_status("978-1/1") == "reserved"  # AC-4.5

def test_cancel_reservation():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    member = Member("member1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    library.cancel_reservation("978-1", member)
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.2

def test_cancel_nonexistent_reservation():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    member = Member("member1")
    with pytest.raises(Exception) as excinfo:
        library.cancel_reservation("978-1", member)  # AC-5.3
    assert "does not have a reservation" in str(excinfo.value)

def test_lapse_uncollected_hold():
    library = Library()
    library.add_title("978-1", "Title A", "Category A", "Shelf A")
    member = Member("member1")
    library.add_copy("978-1")
    library.reserve("978-1", member)
    library.set_current_date("2023-10-05")  # Simulating hold lapse on day 4
    assert library.get_copy_status("978-1/1") == "available"  # AC-5.5