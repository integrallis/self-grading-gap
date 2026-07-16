# file: alarm_system/loud_alarm.py
from candidate.impl import LoudAlarm as _LoudAlarm

class LoudAlarm:
    def trigger(self):
        return _LoudAlarm().trigger()
