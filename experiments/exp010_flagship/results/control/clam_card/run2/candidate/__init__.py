class TransitCard:
    def __init__(self):
        self.journeys = []
        self.total = 0.0
        self.prices = {
            'Aldgate': 2.50,
            'Angel': 2.50,
            'Balham': 3.00,
            'Barbican': 3.00,
        }
        self.daily_cap = 8.00
        self.weekly_cap = 40.00
        self.monthly_cap = 145.00
        self.current_date = None
        self.daily_total = 0.0
        self.journeys_per_day = {}  # To track journeys per day

    def add_journey(self, start, end, date):
        if start not in self.prices and end not in self.prices:
            return None
        if date != self.current_date:
            self.current_date = date
            self.daily_total = 0.0
            self.journeys_per_day = {}

        charge = self.calculate_charge(start, end)
        if charge is None:
            return None

        # Daily cap check
        if self.daily_total + charge > self.daily_cap:
            charge = self.daily_cap - self.daily_total

        # Update totals
        self.daily_total += charge
        self.total += charge
        self.journeys.append((start, end, date, charge))

        # Weekly cap check
        if date not in self.journeys_per_day:
            self.journeys_per_day[date] = 0
        self.journeys_per_day[date] += charge
        weekly_total = sum(self.journeys_per_day.values())
        if weekly_total > self.weekly_cap:
            excess = weekly_total - self.weekly_cap
            self.total -= excess
            self.daily_total -= excess

        # Monthly cap check
        if self.current_date[:7] not in self.journeys_per_day:
            self.journeys_per_day[self.current_date[:7]] = 0
        self.journeys_per_day[self.current_date[:7]] += charge
        monthly_total = sum(self.journeys_per_day.values())
        if monthly_total > self.monthly_cap:
            excess = monthly_total - self.monthly_cap
            self.total -= excess
            self.daily_total -= excess

        return charge

    def calculate_charge(self, start, end):
        if start not in self.prices:
            return None
        if end not in self.prices:
            return None
        if start == end:
            return self.prices[start]
        return max(self.prices[start], self.prices[end])

    def get_total(self):
        return self.total
