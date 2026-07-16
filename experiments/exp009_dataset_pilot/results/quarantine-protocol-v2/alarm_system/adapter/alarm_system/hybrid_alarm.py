# file: alarm_system/hybrid_alarm.py
from candidate.impl import HybridAlarm as _HybridAlarm

class HybridAlarm:
    def __init__(self, alarms):
        self._alarm = _HybridAlarm(alarms)

    def trigger(self):
        return self._alarm.trigger()
