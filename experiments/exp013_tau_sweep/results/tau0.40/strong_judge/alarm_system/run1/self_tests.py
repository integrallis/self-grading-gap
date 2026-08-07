# test_solution.py

from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm_triggers_correctly():
    # Triggering the loud alarm should produce "LOUD ALARM!"
    alarm = LoudAlarm()
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_sounds_day():
    # When it is day, the wrapped alarm should sound unchanged
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    assert day_night_alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_sounds_night():
    # When it is night, the alarm should produce silence
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    assert day_night_alarm.trigger() == ""

def test_hybrid_alarm_sounds_all_alarms():
    # A hybrid alarm with two loud alarms should concatenate their sounds
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Expected: "LOUD ALARM! LOUD ALARM!" (two sounds separated by a space)
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"

def test_hybrid_alarm_sounds_one_alarm():
    # A hybrid alarm with one loud alarm should just sound that alarm
    alarm = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm])
    assert hybrid_alarm.trigger() == "LOUD ALARM!"

def test_hybrid_alarm_sounds_no_alarms():
    # A hybrid alarm with no alarms should produce no sound
    hybrid_alarm = HybridAlarm([])
    assert hybrid_alarm.trigger() == ""