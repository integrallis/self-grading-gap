# candidate/impl.py

from datetime import datetime, timedelta
from collections import defaultdict

class UnknownStationError(Exception):
    pass

class TransitCard:
    ZONE_A_STATIONS = {'Aldgate', 'Amersham', 'Anerley', 'Angel', 'Asterisk'}
    ZONE_B_STATIONS = {'Balham', 'Barbican', 'Bison', 'Bugel', 'Bullhead'}
    
    FARE_A = 2.50
    FARE_B = 3.00
    DAILY_CAP_A = 7.00
    DAILY_CAP_B = 8.00
    WEEKLY_CAP_A = 40.00
    MONTHLY_CAP_A = 145.00
    WEEKLY_CAP_B = 47.00
    MONTHLY_CAP_B = 165.00

    def __init__(self):
        self.total_charged = 0.0
        self.daily_totals = defaultdict(float)
        self.weekly_totals = defaultdict(float)
        self.monthly_totals = defaultdict(float)
        self.last_journey_date = None

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

    def _calculate_fare(self, zone):
        if zone == 'A':
            return self.FARE_A
        else:
            return self.FARE_B

    def _apply_daily_cap(self, fare, zone, journey_date):
        cap = self.DAILY_CAP_A if zone == 'A' else self.DAILY_CAP_B
        if journey_date != self.last_journey_date:
            self.daily_totals[journey_date] = 0.0
        available_cap = cap - self.daily_totals[journey_date]
        if available_cap <= 0:
            return 0.0
        charge = min(fare, available_cap)
        self.daily_totals[journey_date] += charge
        return charge

    def _apply_weekly_cap(self, fare, zone, journey_date):
        iso_week = journey_date.isocalendar()[1]
        if zone == 'A':
            cap = self.WEEKLY_CAP_A
        else:
            cap = self.WEEKLY_CAP_B
        
        if journey_date not in self.weekly_totals or journey_date.isocalendar()[1] != self.last_journey_date.isocalendar()[1]:
            self.weekly_totals[journey_date] = 0.0
            
        total_weekly = self.weekly_totals[journey_date]
        if total_weekly + fare > cap:
            return 0.0
        self.weekly_totals[journey_date] += fare
        return fare

    def _apply_monthly_cap(self, fare, zone, journey_date):
        month = journey_date.replace(day=1)
        if zone == 'A':
            cap = self.MONTHLY_CAP_A
        else:
            cap = self.MONTHLY_CAP_B
        
        if month not in self.monthly_totals:
            self.monthly_totals[month] = 0.0
            
        total_monthly = self.monthly_totals[month]
        if total_monthly + fare > cap:
            return 0.0
        self.monthly_totals[month] += fare
        return fare

    def travel(self, origin, destination, journey_date):
        journey_date = datetime.strptime(journey_date, '%Y-%m-%d').date()
        try:
            zone = self._get_zones(origin, destination)
        except UnknownStationError as e:
            print(e)
            return 0.0  # No charge for failed journey

        fare = self._calculate_fare(zone)
        daily_charge = self._apply_daily_cap(fare, zone, journey_date)
        weekly_charge = self._apply_weekly_cap(daily_charge, zone, journey_date)
        monthly_charge = self._apply_monthly_cap(weekly_charge, zone, journey_date)

        self.total_charged += monthly_charge
        self.last_journey_date = journey_date

        return monthly_charge

    def get_total_charged(self):
        return self.total_charged
