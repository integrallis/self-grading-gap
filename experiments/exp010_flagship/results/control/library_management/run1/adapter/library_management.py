# file: library_management.py
from candidate import DuplicateReservationError
from candidate import Library as _Library
from candidate import UnknownBookError
from candidate import UnknownMemberError
from candidate import Member as _Member


LibraryError = ValueError
NoAvailableCopyError = ValueError
UnknownCopyError = ValueError


class Library(_Library):
    def __init__(self, current_date, loan_period, fine_rate):
        super().__init__()
        self.set_current_date(current_date)

    def add_book(self, isbn, title, genre=None, shelf=None):
        return self.add_title(isbn, title, genre, shelf)

    def register_member(self, member_id, name):
        return _Member(member_id)

    def available_copies(self, isbn):
        return self.get_available_count(isbn)

    def book_info(self, isbn):
        return self.get_title_details(isbn)

    def status(self, copy_id):
        return self.get_copy_status(copy_id)

    def advance(self, duration):
        return self.set_current_date(self.get_current_date().__add__(duration))

    def checkout(self, isbn, member_id):
        return super().checkout(isbn, _Member(member_id))

    def return_copy(self, copy_id):
        return super().return_copy(copy_id, _Member(self.checked_out.get(copy_id)))

    def reserve(self, isbn, member_id):
        return super().reserve(isbn, _Member(member_id))

    def cancel_reservation(self, isbn, member_id):
        return super().cancel_reservation(isbn, _Member(member_id))
