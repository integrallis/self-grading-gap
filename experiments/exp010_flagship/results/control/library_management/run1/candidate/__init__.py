class UnknownBookError(ValueError):
    pass

class UnknownMemberError(ValueError):
    pass

class DuplicateReservationError(ValueError):
    pass

class ReservationError(ValueError):
    pass

from datetime import datetime, timedelta

class Member:
    def __init__(self, member_id):
        self.member_id = member_id

class Library:
    def __init__(self):
        self.titles = {}
        self.copies = {}
        self.checked_out = {}
        self.reserved = {}
        self.current_date = datetime.now()

    def add_title(self, isbn, title, genre, shelf):
        self.titles[isbn] = (title, genre, shelf)

    def add_copy(self, isbn):
        if isbn not in self.copies:
            self.copies[isbn] = []
        copy_id = f"{isbn}/{len(self.copies[isbn]) + 1}"
        self.copies[isbn].append(copy_id)

    def get_copy_status(self, copy_id):
        if copy_id in self.checked_out:
            return "checked_out"
        for isbn, copies in self.copies.items():
            if copy_id in copies:
                return "available"
        raise ValueError(f"Unknown copy identifier: {copy_id}")

    def get_title_details(self, isbn):
        return self.titles[isbn]

    def get_copy_identifier(self, isbn, number):
        return f"{isbn}/{number}"

    def remove_copy(self, copy_id):
        if copy_id in self.checked_out:
            raise ValueError(f"Copy {copy_id} not available for removal")
        for isbn, copies in self.copies.items():
            if copy_id in copies:
                self.copies[isbn].remove(copy_id)
                return
        raise ValueError(f"Unknown copy identifier: {copy_id}")

    def checkout(self, isbn, member):
        if isbn not in self.titles:
            raise UnknownBookError(f"Unknown book: {isbn}")
        if len(self.copies[isbn]) == 0:
            raise ValueError(f"No copies of {isbn} are available")
        copy_id = self.copies[isbn][0]
        self.checked_out[copy_id] = member.member_id
        self.copies[isbn].remove(copy_id)

    def return_copy(self, copy_id, member):
        if copy_id not in self.checked_out:
            raise ValueError(f"Copy {copy_id} is not checked out")
        if self.checked_out[copy_id] != member.member_id:
            raise ValueError(f"Copy {copy_id} is not checked out by this member")
        del self.checked_out[copy_id]
        self.copies[copy_id.split('/')[0]].append(copy_id)

    def reserve(self, isbn, member):
        if isbn not in self.titles:
            raise UnknownBookError(f"Unknown book: {isbn}")
        if isbn not in self.reserved:
            self.reserved[isbn] = []
        if member.member_id in self.reserved[isbn]:
            raise DuplicateReservationError(f"{member.member_id} already has a reservation")
        self.reserved[isbn].append(member.member_id)

    def cancel_reservation(self, isbn, member):
        if isbn not in self.reserved or member.member_id not in self.reserved[isbn]:
            raise ValueError(f"{member.member_id} has no reservation for {isbn}")
        self.reserved[isbn].remove(member.member_id)

    def set_current_date(self, date):
        self.current_date = date

    def get_current_date(self):
        return self.current_date

    def get_fine(self, member):
        for copy_id, m_id in self.checked_out.items():
            if m_id == member.member_id:
                return max(0, (self.current_date - (self.get_due_date(copy_id.split('/')[0], member))).days) * 0.5
        return 0

    def get_due_date(self, isbn, member):
        return self.current_date + timedelta(days=14)

    def get_available_count(self, isbn):
        return len(self.copies[isbn])

    def get_reserving_member(self, copy_id):
        for isbn, members in self.reserved.items():
            if copy_id.split('/')[0] == isbn:
                return members[0] if members else None
        return None
