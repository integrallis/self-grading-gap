from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm_triggers_sound():
    alarm = LoudAlarm()
    assert alarm.trigger() == "LOUD ALARM!"  # AC-1.1

def test_day_night_switched_alarm_sounds_during_day():
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    assert day_night_alarm.trigger() == "LOUD ALARM!"  # AC-2.1

def test_day_night_switched_alarm_silence_during_night():
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    assert day_night_alarm.trigger() == ""  # AC-2.2

def test_hybrid_alarm_triggers_combined_sounds():
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"  # AC-3.1