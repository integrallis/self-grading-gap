from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm_sounds():
    # Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    loud_alarm = LoudAlarm()
    assert loud_alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_sounds_day():
    # When it is day, triggering it produces the wrapped alarm's sound unchanged.
    loud_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(loud_alarm, is_day=True)
    assert day_night_alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_sounds_night():
    # When it is night, triggering it produces silence (an empty sound report).
    loud_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(loud_alarm, is_day=False)
    assert day_night_alarm.trigger() == ""

def test_hybrid_alarm_sounds():
    # Triggering it produces the sounds of all of its member alarms combined into one report.
    loud_alarm1 = LoudAlarm()
    loud_alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([loud_alarm1, loud_alarm2])
    # Two loud alarms together produce "LOUD ALARM! LOUD ALARM!".
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"