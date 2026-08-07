from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

def test_loud_alarm_triggers_sound():
    alarm = LoudAlarm()
    # Triggering the loud alarm produces exactly the sound report "LOUD ALARM!".
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switch_day_with_loud_alarm():
    wrapped_alarm = LoudAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    # When it is day, triggering it produces the wrapped alarm's sound unchanged.
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switch_night_with_loud_alarm():
    wrapped_alarm = LoudAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    # When it is night, triggering it produces silence (an empty sound report).
    assert alarm.trigger() == ""

def test_day_night_switch_day_with_custom_alarm():
    class CustomAlarm:
        def trigger(self):
            return "CUSTOM ALARM!"

    wrapped_alarm = CustomAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    # When it is day, it should produce the wrapped alarm's sound unchanged.
    assert alarm.trigger() == "CUSTOM ALARM!"

def test_day_night_switch_night_with_custom_alarm():
    class CustomAlarm:
        def trigger(self):
            return "CUSTOM ALARM!"

    wrapped_alarm = CustomAlarm()
    alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    # When it is night, triggering it produces silence (an empty sound report).
    assert alarm.trigger() == ""

def test_hybrid_alarm_triggers_combined_sounds():
    class FirstAlarm:
        def trigger(self):
            return "FIRST"

    class SecondAlarm:
        def trigger(self):
            return "SECOND"

    alarm1 = FirstAlarm()
    alarm2 = SecondAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Triggering it produces the sounds of all of its member alarms combined into one report,
    # separated by a single space.
    assert hybrid_alarm.trigger() == "FIRST SECOND"

def test_hybrid_alarm_triggers_multiple_loud_alarms():
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    alarm3 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2, alarm3])
    # Triggering it produces the sounds of all of its member alarms combined into one report,
    # separated by a single space.
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM! LOUD ALARM!"