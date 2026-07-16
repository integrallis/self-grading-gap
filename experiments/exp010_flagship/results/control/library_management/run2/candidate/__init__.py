class Library:
    def __init__(self):
        self.titles = {}
        self.copies = {}
        self.checked_out = {}
        self.reservations = {}

    def add_title(self, isbn, title, genre, location):
        self.titles[isbn] = (title, genre, location)

    def add_copy(self, isbn):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        copy_id = f"{isbn}/{len([cid for cid in self.copies if cid.startswith(isbn)]) + 1}"
        self.copies[copy_id] = 'available'
        return copy_id

    def get_copy_status(self, copy_id):
        if copy_id not in self.copies:
            raise ValueError(f"Unknown copy identifier: {copy_id}")
        return self.copies[copy_id]

    def get_available_count(self, isbn):
        return sum(1 for cid in self.copies if cid.startswith(isbn) and self.copies[cid] == 'available')

    def get_title_info(self, isbn):
        return (isbn, *self.titles[isbn])

    def remove_copy(self, copy_id):
        if copy_id not in self.copies:
            raise ValueError(f"Unknown copy identifier: {copy_id}")
        if self.copies[copy_id] != 'available':
            raise ValueError("Copy is not available for removal.")
        del self.copies[copy_id]

    def checkout(self, copy_id, member):
        if copy_id not in self.copies:
            raise ValueError(f"Unknown book: {copy_id}")
        if self.copies[copy_id] != 'available':
            raise ValueError(f"No copies of {copy_id.split('/')[0]} are available.")
        self.copies[copy_id] = 'checked_out'
        self.checked_out[copy_id] = member
        return "2023-10-01"  # Placeholder for due date

    def return_copy(self, copy_id, member, due_date):
        if copy_id not in self.copies:
            raise ValueError(f"Unknown copy identifier: {copy_id}")
        if self.copies[copy_id] != 'checked_out':
            raise ValueError("Copy is not checked out.")
        self.copies[copy_id] = 'available'
        # Calculate fine
        fine = 0.0
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d')
        today = datetime.now()
        if today > due_date_obj:
            days_late = (today - due_date_obj).days
            fine = days_late * 0.5  # Assuming a fine of $0.5 per day late
        return fine

    def reserve(self, isbn, member):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        if member in self.reservations.get(isbn, []):
            raise ValueError("Member already has a reservation.")
        if self.get_available_count(isbn) == 0:
            self.reservations.setdefault(isbn, []).append(member)
            for cid in self.copies:
                if cid.startswith(isbn) and self.copies[cid] == 'available':
                    self.copies[cid] = 'reserved'
                    break

    def cancel_reservation(self, isbn, member):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        if member not in self.reservations.get(isbn, []):
            raise ValueError("Member has no reservation for this ISBN.")
        self.reservations[isbn].remove(member)
        if not self.reservations[isbn]:
            del self.reservations[isbn]

    def lapse_hold(self, isbn):
        if isbn in self.reservations:
            del self.reservations[isbn]
            for cid in self.copies:
                if cid.startswith(isbn) and self.copies[cid] == 'reserved':
                    self.copies[cid] = 'available'

    def get_reservation_status(self, member, isbn):
        if isbn not in self.titles:
            raise ValueError(f"Unknown book: {isbn}")
        if member in self.reservations.get(isbn, []):
            return "reserved"
        return "not_reserved"

class Member:
    def __init__(self, member_id):
        self.member_id = member_id

class Copy:
    pass

class Reservation:
    pass