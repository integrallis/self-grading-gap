from solution import LoudAlarm, DayNightAlarm, HybridAlarm

def test_loud_alarm_triggers_correctly():
    alarm = LoudAlarm()  # Assuming a loud alarm is created with a specific constructor
    assert alarm.trigger() == "LOUD ALARM!"  # AC-1.1

def test_day_night_switched_alarm_sounds_during_day():
    wrapped_alarm = LoudAlarm()  # Wrap a loud alarm
    day_night_alarm = DayNightAlarm(wrapped_alarm, is_day=True)  # Daytime
    assert day_night_alarm.trigger() == "LOUD ALARM!"  # AC-2.1

def test_day_night_switched_alarm_sounds_nothing_at_night():
    wrapped_alarm = LoudAlarm()  # Wrap a loud alarm
    day_night_alarm = DayNightAlarm(wrapped_alarm, is_day=False)  # Nighttime
    assert day_night_alarm.trigger() == ""  # AC-2.2

def test_hybrid_alarm_sounds_combined_loud_alarms():
    alarm1 = LoudAlarm()  # First loud alarm
    alarm2 = LoudAlarm()  # Second loud alarm
    hybrid_alarm = HybridAlarm([alarm1, alarm2])  # Create a hybrid alarm with two loud alarms
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"  # AC-3.1