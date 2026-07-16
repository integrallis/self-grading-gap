# file: alarm_system/hybrid_alarm.py
from candidate.impl import HybridAlarm as _HybridAlarm

class HybridAlarm(_HybridAlarm):
    def __init__(self, alarms):
        super().__init__(alarms)

    def trigger(self):
        return super().trigger()
