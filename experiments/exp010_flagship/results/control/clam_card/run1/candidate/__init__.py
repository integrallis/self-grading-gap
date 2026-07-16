class TransitCard:
    def __init__(self):
        self.total = 0.0
        self.journeys = []
        self.daily_totals = {}
        self.weekly_totals = {}
        self.monthly_totals = {}
        self.daily_cap = 7.00
        self.weekly_cap = 40.00
        self.monthly_cap = 145.00
        self.zones = {
            'Aldgate': 'A',
            'Anerley': 'A',
            'Angel': 'A',
            'Balham': 'B',
            'Barbican': 'B',
            'Bison': 'B',
            'Bugel': 'B'
        }

    def take_journey(self, start, end, date):
        if start not in self.zones or end not in self.zones:
            return f'unknown-station: {start if start not in self.zones else end}'

        zone_start = self.zones[start]
        zone_end = self.zones[end]

        if zone_start == zone_end:
            amount = 2.50 if zone_start == 'A' else 3.00
        else:
            amount = 3.00

        if date not in self.daily_totals:
            self.daily_totals[date] = 0.0
        if date not in self.weekly_totals:
            self.weekly_totals[date] = 0.0
        if date not in self.monthly_totals:
            self.monthly_totals[date] = 0.0

        daily_total = self.daily_totals[date]
        weekly_total = sum(self.daily_totals.get(d, 0) for d in self.daily_totals if d == date)
        monthly_total = sum(self.daily_totals.get(d, 0) for d in self.daily_totals if d.startswith(date[:7]))

        if daily_total + amount > self.daily_cap:
            excess_amount = daily_total + amount - self.daily_cap
            if zone_start == 'A':
                amount = max(0, amount - excess_amount)
            else:
                amount = max(0, amount)

        if amount > 0:
            self.total += amount
            self.daily_totals[date] += amount
            self.weekly_totals[date] = weekly_total + amount
            self.monthly_totals[date] = monthly_total + amount

            if self.weekly_totals[date] > self.weekly_cap:
                self.weekly_totals[date] = self.weekly_cap
            if self.monthly_totals[date] > self.monthly_cap:
                self.monthly_totals[date] = self.monthly_cap

        return amount

    def get_total(self):
        return self.total
