from solution import Alarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm():
    alarm = Alarm()  # Assuming a loud alarm is created without parameters
    # Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_day():
    wrapped_alarm = Alarm()  # Assuming this wraps a loud alarm
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    # When it is day, triggering it produces the wrapped alarm's sound unchanged.
    assert alarm.trigger() == "LOUD ALARM!"  # Expected output from the loud alarm

def test_day_night_switched_alarm_night():
    wrapped_alarm = Alarm()  # Assuming this wraps a loud alarm
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    # When it is night, triggering it produces silence (an empty sound report).
    assert alarm.trigger() == ""

def test_hybrid_alarm():
    alarm1 = Alarm()  # First loud alarm
    alarm2 = Alarm()  # Second loud alarm
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Triggering it produces the sounds of all of its member alarms combined into one report.
    # "LOUD ALARM! LOUD ALARM!" is the expected output.
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"