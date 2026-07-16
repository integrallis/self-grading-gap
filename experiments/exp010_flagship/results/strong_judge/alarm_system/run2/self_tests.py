from solution import LoudAlarm, DayNightAlarm, HybridAlarm

def test_loud_alarm_sounds():
    # AC-1.1: Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    alarm = LoudAlarm()
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_alarm_sounds_day():
    # AC-2.1: When it is day, triggering it produces the wrapped alarm's sound unchanged.
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightAlarm(wrapped_alarm, is_day=True)
    assert day_night_alarm.trigger() == "LOUD ALARM!"

def test_day_night_alarm_sounds_night():
    # AC-2.2: When it is night, triggering it produces silence (an empty sound report).
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightAlarm(wrapped_alarm, is_day=False)
    assert day_night_alarm.trigger() == ""

def test_hybrid_alarm_sounds():
    # AC-3.1: Triggering it produces the sounds of all its member alarms combined into one report.
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Triggering two loud alarms together produces "LOUD ALARM! LOUD ALARM!".
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"