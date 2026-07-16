class Title:
    def __init__(self, isbn, title, genre, location):
        self.isbn = isbn
        self.title = title
        self.genre = genre
        self.location = location

class Copy:
    def __init__(self, title, copy_number):
        self.title = title
        self.copy_number = copy_number
        self.status = 'available'
        self.member_id = None
        self.due_date = None

class Member:
    def __init__(self, member_id):
        self.member_id = member_id

class Library:
    def __init__(self):
        self.titles = {}
        self.copies = {}
        self.reservations = {}

    def add_title(self, title):
        self.titles[title.isbn] = title
        self.copies[title.isbn] = []

    def add_copy(self, isbn):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        copy_number = len(self.copies[isbn]) + 1
        new_copy = Copy(isbn, copy_number)
        self.copies[isbn].append(new_copy)

    def get_copy_identifier(self, isbn, copy_number):
        return f"{isbn}/{copy_number}"

    def get_copy_status(self, copy_identifier):
        isbn, copy_number = copy_identifier.split('/')
        copy_number = int(copy_number) - 1
        if isbn not in self.copies or copy_number >= len(self.copies[isbn]):
            raise ValueError(f"Unknown copy identifier: {copy_identifier}")
        return self.copies[isbn][copy_number].status

    def get_available_copies_count(self, isbn):
        if isbn not in self.copies:
            raise ValueError(f"Unknown book: {isbn}")
        return sum(1 for copy in self.copies[isbn] if copy.status == 'available')

    def get_title_details(self, isbn):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        title = self.titles[isbn]
        return (title.isbn, title.title, title.genre, title.location)

    def checkout_copy(self, member_id, isbn):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        if member_id not in self.reservations:
            self.reservations[member_id] = []
        available_copies = [copy for copy in self.copies[isbn] if copy.status == 'available']
        if not available_copies:
            raise ValueError(f"No copies of {isbn} are available")
        copy_to_checkout = available_copies[0]
        copy_to_checkout.status = 'checked_out'
        copy_to_checkout.member_id = member_id
        return self._set_due_date(copy_to_checkout)

    def _set_due_date(self, copy):
        # Assuming a due date of 14 days from checkout
        copy.due_date = 14  # Placeholder for actual date logic
        return copy.due_date

    def remove_copy(self, copy_identifier):
        isbn, copy_number = copy_identifier.split('/')
        copy_number = int(copy_number) - 1
        if isbn not in self.copies or copy_number >= len(self.copies[isbn]):
            raise ValueError(f"Unknown copy identifier: {copy_identifier}")
        copy = self.copies[isbn][copy_number]
        if copy.status != 'available':
            raise ValueError(f"Copy '{copy_identifier}' not available for removal")
        del self.copies[isbn][copy_number]

    def return_copy(self, copy_identifier, member):
        isbn, copy_number = copy_identifier.split('/')
        copy_number = int(copy_number) - 1
        if isbn not in self.copies or copy_number >= len(self.copies[isbn]):
            raise ValueError(f"Unknown copy identifier: {copy_identifier}")
        copy = self.copies[isbn][copy_number]
        if copy.status != 'checked_out':
            raise ValueError(f"Copy '{copy_identifier}' is not checked out")
        copy.status = 'available'
        copy.member_id = None
        fine = self._calculate_fine(copy)
        return fine

    def _calculate_fine(self, copy):
        # Placeholder fine logic: if overdue, charge $1.50
        if copy.due_date < 0:  # Simulating overdue check
            return 1.50
        return 0.0

    def reserve_title(self, member_id, isbn):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        if member_id not in self.reservations:
            self.reservations[member_id] = []
        self.reservations[member_id].append(isbn)
        for copy in self.copies[isbn]:
            if copy.status == 'available':
                copy.status = 'reserved'
                return

    def cancel_reservation(self, member_id, isbn):
        if member_id not in self.reservations or isbn not in self.reservations[member_id]:
            raise ValueError(f"Member does not have a reservation for ISBN: {isbn}")
        self.reservations[member_id].remove(isbn)
        for copy in self.copies[isbn]:
            if copy.status == 'reserved':
                copy.status = 'available'
                return

    def set_hold_period(self, days):
        self.hold_period = days

    def check_expired_holds(self):
        for member_id, holds in self.reservations.items():
            for isbn in holds:
                for copy in self.copies[isbn]:
                    if copy.status == 'reserved':
                        copy.status = 'available'  # Release hold