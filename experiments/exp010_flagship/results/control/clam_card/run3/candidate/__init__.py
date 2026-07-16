class TransitCard:
    def __init__(self):
        self.journeys = []
        self.daily_cap = 7.00
        self.weekly_cap = 40.00
        self.monthly_cap = 145.00
        self.zone_fares = {
            'A': 2.50,
            'B': 3.00
        }
        self.total_charges = {}  # Tracks total for each day

    def journey(self, start, end, date):
        if start not in self.zone_fares and end not in self.zone_fares:
            return 0.00

        fare = self.calculate_fare(start, end)
        if fare == 0:
            return 0.00

        self.record_journey(date, fare)
        return fare

    def calculate_fare(self, start, end):
        zone_start = self.get_zone(start)
        zone_end = self.get_zone(end)
        if zone_start == zone_end:
            return self.zone_fares.get(zone_start, 0)
        elif zone_start and zone_end:
            return self.zone_fares['B']  # Zone A to Zone B
        return self.zone_fares.get(zone_end, 0)

    def get_zone(self, station):
        if station in ['Aldgate', 'Anerley']:
            return 'A'
        elif station in ['Balham', 'Barbican']:
            return 'B'
        return None

    def record_journey(self, date, fare):
        if date not in self.total_charges:
            self.total_charges[date] = 0
        # Check daily cap
        self.total_charges[date] += fare
        if self.total_charges[date] > self.daily_cap:
            self.total_charges[date] = self.daily_cap

    def total(self):
        return sum(min(charge, self.daily_cap) for charge in self.total_charges.values())
