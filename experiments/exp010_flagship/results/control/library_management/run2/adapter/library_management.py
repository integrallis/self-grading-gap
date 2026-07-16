# file: library_management.py
from candidate import Library as _CandidateLibrary

LibraryError = ValueError
UnknownBookError = ValueError
UnknownCopyError = ValueError
UnknownMemberError = ValueError
NoAvailableCopyError = ValueError
DuplicateReservationError = ValueError


class Library(_CandidateLibrary):
    def __init__(self, *args):
        _CandidateLibrary.__init__(self)

    def add_book(self, isbn, title, genre=None, location=None):
        return self.add_title(isbn, title, genre, location)

    def available_copies(self, isbn):
        return self.get_available_count(isbn)

    def book_info(self, isbn):
        return self.get_title_info(isbn)

    def status(self, copy_id):
        return self.get_copy_status(copy_id)

    def advance(self, isbn):
        return self.lapse_hold(isbn)
