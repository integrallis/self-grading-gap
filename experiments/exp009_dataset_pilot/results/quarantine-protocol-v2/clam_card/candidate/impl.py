# candidate/impl.py

from datetime import datetime, timedelta
from collections import defaultdict

class UnknownStationError(Exception):
    pass

class TransitCard:
    ZONE_A_FARE = 2.50
    ZONE_B_FARE = 3.00
    DAILY_CAP_A = 7.00
    DAILY_CAP_B = 8.00
    WEEKLY_CAP_A = 40.00
    MONTHLY_CAP_A = 145.00
    WEEKLY_CAP_B = 47.00
    MONTHLY_CAP_B = 165.00

    ZONE_A_STATIONS = {'Aldgate', 'Amersham', 'Anerley', 'Angel', 'Asterisk'}
    ZONE_B_STATIONS = {'Balham', 'Barbican', 'Bison', 'Bugel', 'Bullhead'}

    def __init__(self):
        self.total_charged = 0.0
        self.daily_totals = defaultdict(float)
        self.weekly_totals = defaultdict(float)
        self.monthly_totals = defaultdict(float)

    def charge_journey(self, origin, destination, journey_date):
        if origin not in self.ZONE_A_STATIONS and origin not in self.ZONE_B_STATIONS:
            raise UnknownStationError(f"Unknown station: {origin}")
        if destination not in self.ZONE_A_STATIONS and destination not in self.ZONE_B_STATIONS:
            raise UnknownStationError(f"Unknown station: {destination}")

        fare, zone = self._calculate_fare(origin, destination)
        day_key = journey_date.date()
        week_key = self._get_iso_week(journey_date)
        month_key = journey_date.month

        daily_cap = self.DAILY_CAP_A if zone == 'A' else self.DAILY_CAP_B
        if self.daily_totals[day_key] < daily_cap:
            remaining_cap = daily_cap - self.daily_totals[day_key]
            if fare <= remaining_cap:
                charge = fare
            else:
                charge = remaining_cap
            self.daily_totals[day_key] += charge
        else:
            charge = 0.0

        # Adjust for weekly and monthly caps
        if charge > 0:
            self._apply_weekly_cap(week_key, charge, zone)
            self._apply_monthly_cap(month_key, charge, zone)

        self.total_charged += charge
        return charge

    def _calculate_fare(self, origin, destination):
        if origin in self.ZONE_A_STATIONS and destination in self.ZONE_A_STATIONS:
            return self.ZONE_A_FARE, 'A'
        else:
            return self.ZONE_B_FARE, 'B'

    def _get_iso_week(self, date):
        return date.isocalendar()[0], date.isocalendar()[1]

    def _apply_weekly_cap(self, week_key, charge, zone):
        weekly_cap = self.WEEKLY_CAP_A if zone == 'A' else self.WEEKLY_CAP_B
        if self.weekly_totals[week_key] + charge > weekly_cap:
            self.weekly_totals[week_key] = weekly_cap
        else:
            self.weekly_totals[week_key] += charge

    def _apply_monthly_cap(self, month_key, charge, zone):
        monthly_cap = self.MONTHLY_CAP_A if zone == 'A' else self.MONTHLY_CAP_B
        if self.monthly_totals[month_key] + charge > monthly_cap:
            self.monthly_totals[month_key] = monthly_cap
        else:
            self.monthly_totals[month_key] += charge

    def get_total_charged(self):
        return self.total_charged
