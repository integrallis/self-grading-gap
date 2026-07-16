# candidate/impl.py

class TransitCard:
    ZONE_A_STATIONS = {"Aldgate", "Amersham", "Anerley", "Angel", "Asterisk"}
    ZONE_B_STATIONS = {"Balham", "Barbican", "Bison", "Bugel", "Bullhead"}

    ZONE_A_FARE = 2.50
    ZONE_B_FARE = 3.00
    ZONE_A_DAILY_CAP = 7.00
    ZONE_B_DAILY_CAP = 8.00
    ZONE_A_WEEKLY_CAP = 40.00
    ZONE_B_WEEKLY_CAP = 47.00
    ZONE_A_MONTHLY_CAP = 145.00
    ZONE_B_MONTHLY_CAP = 165.00

    def __init__(self):
        self.total_charged = 0.0
        self.daily_totals = {}
        self.weekly_totals = {}
        self.monthly_totals = {}
        self.journey_dates = {}

    def _get_zones(self, origin, destination):
        if origin in self.ZONE_A_STATIONS and destination in self.ZONE_A_STATIONS:
            return 'A'
        elif origin in self.ZONE_B_STATIONS and destination in self.ZONE_B_STATIONS:
            return 'B'
        elif (origin in self.ZONE_A_STATIONS and destination in self.ZONE_B_STATIONS) or \
             (origin in self.ZONE_B_STATIONS and destination in self.ZONE_A_STATIONS):
            return 'B'
        else:
            raise ValueError(f"Unknown station(s): {origin}, {destination}")

    def _get_fare(self, zone):
        if zone == 'A':
            return self.ZONE_A_FARE
        elif zone == 'B':
            return self.ZONE_B_FARE

    def _apply_daily_cap(self, date, fare):
        if date not in self.daily_totals:
            self.daily_totals[date] = 0.0

        if fare + self.daily_totals[date] > (self.ZONE_B_DAILY_CAP if 'B' in self.journey_dates[date] else self.ZONE_A_DAILY_CAP):
            fare = (self.ZONE_B_DAILY_CAP if 'B' in self.journey_dates[date] else self.ZONE_A_DAILY_CAP) - self.daily_totals[date]
            if fare < 0:
                return 0.0

        self.daily_totals[date] += fare
        return fare

    def _reset_weekly_totals(self, date):
        week_start = date - timedelta(days=date.weekday())
        if week_start not in self.weekly_totals:
            self.weekly_totals[week_start] = 0.0

    def _apply_weekly_cap(self, date, fare):
        week_start = date - timedelta(days=date.weekday())
        self._reset_weekly_totals(week_start)

        if fare + self.weekly_totals[week_start] > (self.ZONE_B_WEEKLY_CAP if 'B' in self.journey_dates[week_start] else self.ZONE_A_WEEKLY_CAP):
            fare = (self.ZONE_B_WEEKLY_CAP if 'B' in self.journey_dates[week_start] else self.ZONE_A_WEEKLY_CAP) - self.weekly_totals[week_start]
            if fare < 0:
                return 0.0

        self.weekly_totals[week_start] += fare
        return fare

    def _apply_monthly_cap(self, date, fare):
        month_start = date.replace(day=1)
        if month_start not in self.monthly_totals:
            self.monthly_totals[month_start] = 0.0

        if fare + self.monthly_totals[month_start] > (self.ZONE_B_MONTHLY_CAP if 'B' in self.journey_dates[month_start] else self.ZONE_A_MONTHLY_CAP):
            fare = (self.ZONE_B_MONTHLY_CAP if 'B' in self.journey_dates[month_start] else self.ZONE_A_MONTHLY_CAP) - self.monthly_totals[month_start]
            if fare < 0:
                return 0.0

        self.monthly_totals[month_start] += fare
        return fare

    def charge_journey(self, origin, destination, journey_date):
        try:
            zone = self._get_zones(origin, destination)
        except ValueError as e:
            return 0.0  # Unknown station, charge nothing

        fare = self._get_fare(zone)
        date_str = journey_date.strftime("%Y-%m-%d")
        if date_str not in self.journey_dates:
            self.journey_dates[date_str] = set()

        self.journey_dates[date_str].add(zone)

        # Apply daily cap
        fare = self._apply_daily_cap(date_str, fare)
        # Apply weekly cap
        fare = self._apply_weekly_cap(journey_date, fare)
        # Apply monthly cap
        fare = self._apply_monthly_cap(journey_date, fare)

        self.total_charged += fare
        return fare

    def get_total_charged(self):
        return self.total_charged
