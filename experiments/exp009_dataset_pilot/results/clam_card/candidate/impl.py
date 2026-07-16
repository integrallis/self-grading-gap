# candidate/impl.py

class UnknownStationError(Exception):
    pass


class TransitCard:
    ZONE_A_STATIONS = {'Aldgate', 'Amersham', 'Anerley', 'Angel', 'Asterisk'}
    ZONE_B_STATIONS = {'Balham', 'Barbican', 'Bison', 'Bugel', 'Bullhead'}

    ZONE_A_FARE = 2.50
    ZONE_B_FARE = 3.00
    DAILY_CAP_A = 7.00
    DAILY_CAP_B = 8.00
    WEEKLY_CAP_A = 40.00
    MONTHLY_CAP_A = 145.00
    WEEKLY_CAP_B = 47.00
    MONTHLY_CAP_B = 165.00

    def __init__(self):
        self.total_charged = 0.0
        self.daily_totals = {}
        self.weekly_totals = {}
        self.monthly_totals = {}

    def _get_zones(self, origin, destination):
        if origin in self.ZONE_A_STATIONS and destination in self.ZONE_A_STATIONS:
            return 'A'
        elif origin in self.ZONE_B_STATIONS and destination in self.ZONE_B_STATIONS:
            return 'B'
        elif (origin in self.ZONE_A_STATIONS and destination in self.ZONE_B_STATIONS) or \
             (origin in self.ZONE_B_STATIONS and destination in self.ZONE_A_STATIONS):
            return 'B'
        else:
            raise UnknownStationError(f"Unknown station: {origin if origin not in self.ZONE_A_STATIONS | self.ZONE_B_STATIONS else destination}")

    def _apply_daily_cap(self, fare, date):
        day_key = date.date()
        if day_key not in self.daily_totals:
            self.daily_totals[day_key] = 0.0

        if self.daily_totals[day_key] + fare <= self.DAILY_CAP_A:
            self.daily_totals[day_key] += fare
            return fare
        elif self.daily_totals[day_key] < self.DAILY_CAP_A:
            remaining = self.DAILY_CAP_A - self.daily_totals[day_key]
            self.daily_totals[day_key] += remaining
            return remaining
        else:
            return 0.0

    def _apply_weekly_cap(self, fare, date):
        iso_week_key = date.isocalendar()[:2]
        if iso_week_key not in self.weekly_totals:
            self.weekly_totals[iso_week_key] = 0.0

        if self.weekly_totals[iso_week_key] + fare <= self.WEEKLY_CAP_A:
            self.weekly_totals[iso_week_key] += fare
            return fare
        else:
            return 0.0

    def _apply_monthly_cap(self, fare, date):
        month_key = date.year, date.month
        if month_key not in self.monthly_totals:
            self.monthly_totals[month_key] = 0.0

        if self.monthly_totals[month_key] + fare <= self.MONTHLY_CAP_A:
            self.monthly_totals[month_key] += fare
            return fare
        else:
            return 0.0

    def charge_journey(self, origin, destination, date):
        try:
            zone = self._get_zones(origin, destination)
        except UnknownStationError as e:
            return 0.0  # No charge for unknown station

        fare = self.ZONE_A_FARE if zone == 'A' else self.ZONE_B_FARE
        if zone == 'B' and self.daily_totals.get(date.date(), 0.0) >= self.DAILY_CAP_A:
            fare = fare - (self.daily_totals[date.date()] - self.DAILY_CAP_A)
            fare = max(fare, 0.0)

        daily_charge = self._apply_daily_cap(fare, date)
        weekly_charge = self._apply_weekly_cap(daily_charge, date)
        monthly_charge = self._apply_monthly_cap(weekly_charge, date)

        self.total_charged += monthly_charge
        return monthly_charge

    def get_total_charged(self):
        return self.total_charged
