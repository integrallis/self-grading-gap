from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm():
    # Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    alarm = LoudAlarm()
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_day():
    # When it is day, triggering it produces the wrapped alarm's sound unchanged.
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    assert day_night_alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_night():
    # When it is night, triggering it produces silence (an empty sound report).
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    assert day_night_alarm.trigger() == ""

def test_hybrid_alarm_single_alarm():
    # Triggering a hybrid alarm with a single loud alarm produces "LOUD ALARM!".
    loud_alarm = LoudAlarm()
    hybrid_alarm = HybridAlarm([loud_alarm])
    assert hybrid_alarm.trigger() == "LOUD ALARM!"

def test_hybrid_alarm_multiple_alarms():
    # Triggering a hybrid alarm with two loud alarms produces "LOUD ALARM! LOUD ALARM!".
    loud_alarm_1 = LoudAlarm()
    loud_alarm_2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([loud_alarm_1, loud_alarm_2])
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"

def test_hybrid_alarm_with_day_night_alarm():
    # Triggering a hybrid alarm with a loud alarm and a day/night alarm during the day produces "LOUD ALARM!".
    loud_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(loud_alarm, is_day=True)
    hybrid_alarm = HybridAlarm([loud_alarm, day_night_alarm])
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"

def test_hybrid_alarm_with_day_night_alarm_night():
    # Triggering a hybrid alarm with a loud alarm and a day/night alarm at night produces "LOUD ALARM!".
    loud_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(loud_alarm, is_day=False)
    hybrid_alarm = HybridAlarm([loud_alarm, day_night_alarm])
    assert hybrid_alarm.trigger() == "LOUD ALARM!"