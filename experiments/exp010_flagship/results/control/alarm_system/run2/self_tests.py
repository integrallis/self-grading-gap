from solution import LoudAlarm, DayNightAlarm, HybridAlarm

def test_loud_alarm_triggers_sound():
    alarm = LoudAlarm()
    # Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_alarm_triggers_sound_during_day():
    wrapped_alarm = LoudAlarm()
    alarm = DayNightAlarm(wrapped_alarm, is_day=True)
    # When it is day, triggering it produces the wrapped alarm's sound unchanged.
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_alarm_triggers_silence_during_night():
    wrapped_alarm = LoudAlarm()
    alarm = DayNightAlarm(wrapped_alarm, is_day=False)
    # When it is night, triggering it produces silence (an empty sound report).
    assert alarm.trigger() == ""

def test_hybrid_alarm_triggers_combined_sounds():
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Triggering it produces the sounds of all of its member alarms combined into one report, 
    # separated by a single space ("LOUD ALARM! LOUD ALARM!").
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"