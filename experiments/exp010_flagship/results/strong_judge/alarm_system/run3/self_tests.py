# test_alarm.py

from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm_triggers_sound():
    alarm = LoudAlarm()
    # Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_sounds_day():
    wrapped_alarm = LoudAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    # When it is day, triggering it produces the wrapped alarm's sound unchanged.
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_sounds_night():
    wrapped_alarm = LoudAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    # When it is night, triggering it produces silence (an empty sound report).
    assert alarm.trigger() == ""

def test_hybrid_alarm_combines_sounds():
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Triggering it produces the sounds of all of its member alarms combined into one report,
    # separated by a single space. (Two loud alarms together produce "LOUD ALARM! LOUD ALARM!")
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"