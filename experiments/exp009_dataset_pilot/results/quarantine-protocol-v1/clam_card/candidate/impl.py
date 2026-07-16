# candidate/impl.py

from datetime import datetime, timedelta
from collections import defaultdict

class TransitCard:
    ZONE_A_STATIONS = {"Aldgate", "Amersham", "Anerley", "Angel", "Asterisk"}
    ZONE_B_STATIONS = {"Balham", "Barbican", "Bison", "Bugel", "Bullhead"}
    
    ZONE_A_FARE = 2.50
    ZONE_B_FARE = 3.00
    
    DAILY_CAP_ZONE_A = 7.00
    DAILY_CAP_ZONE_B = 8.00
    
    WEEKLY_CAP_ZONE_A = 40.00
    MONTHLY_CAP_ZONE_A = 145.00
    WEEKLY_CAP_ZONE_B = 47.00
    MONTHLY_CAP_ZONE_B = 165.00
    
    def __init__(self):
        self.total_charged = 0.0
        self.daily_totals = defaultdict(float)
        self.weekly_totals = defaultdict(float)
        self.monthly_totals = defaultdict(float)

    def _get_zones(self, origin, destination):
        if origin in self.ZONE_A_STATIONS and destination in self.ZONE_A_STATIONS:
            return "A"
        elif origin in self.ZONE_B_STATIONS or destination in self.ZONE_B_STATIONS:
            return "B"
        else:
            raise ValueError(f"Unknown station: {origin if origin not in self.ZONE_A_STATIONS | self.ZONE_B_STATIONS else destination}")

    def _charge_journey(self, fare, date):
        day_key = date.date()
        week_key = (date - timedelta(days=date.weekday())).date()
        month_key = date.replace(day=1).date()

        # Daily cap handling
        if fare == self.ZONE_A_FARE:
            if self.daily_totals[day_key] + fare > self.DAILY_CAP_ZONE_A:
                fare = max(0, self.DAILY_CAP_ZONE_A - self.daily_totals[day_key])
                self.daily_totals[day_key] = self.DAILY_CAP_ZONE_A
            else:
                self.daily_totals[day_key] += fare
        elif fare == self.ZONE_B_FARE:
            if self.daily_totals[day_key] + fare > self.DAILY_CAP_ZONE_B:
                fare = max(0, self.DAILY_CAP_ZONE_B - self.daily_totals[day_key])
                self.daily_totals[day_key] = self.DAILY_CAP_ZONE_B
            else:
                self.daily_totals[day_key] += fare
                if self.daily_totals[day_key] > self.DAILY_CAP_ZONE_A:
                    self.daily_totals[day_key] = self.DAILY_CAP_ZONE_B
        
        # Weekly cap handling
        if self.daily_totals[day_key] >= self.DAILY_CAP_ZONE_A:
            if self.weekly_totals[week_key] + self.DAILY_CAP_ZONE_A > self.WEEKLY_CAP_ZONE_A:
                self.weekly_totals[week_key] = self.WEEKLY_CAP_ZONE_A
            else:
                self.weekly_totals[week_key] += self.daily_totals[day_key]
        
        # Monthly cap handling
        if self.weekly_totals[week_key] >= self.WEEKLY_CAP_ZONE_A:
            if self.monthly_totals[month_key] + self.WEEKLY_CAP_ZONE_A > self.MONTHLY_CAP_ZONE_A:
                self.monthly_totals[month_key] = self.MONTHLY_CAP_ZONE_A
            else:
                self.monthly_totals[month_key] += self.weekly_totals[week_key]

        self.total_charged += fare
        return fare

    def charge_journey(self, origin, destination, journey_date):
        try:
            zones = self._get_zones(origin, destination)
            fare = self.ZONE_A_FARE if zones == "A" else self.ZONE_B_FARE
            return self._charge_journey(fare, journey_date)
        except ValueError as e:
            return 0.0  # No charge for unknown stations

    def get_total_charged(self):
        return self.total_charged
