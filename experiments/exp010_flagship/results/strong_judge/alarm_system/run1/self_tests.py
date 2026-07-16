from solution import LoudAlarm, DayNightSwitchedAlarm, HybridAlarm

class FakeAlarm:
    def __init__(self, sound):
        self.sound = sound
        
    def trigger(self):
        return self.sound

def test_loud_alarm_triggers_sound():
    alarm = LoudAlarm()
    # Triggering the loud alarm should produce "LOUD ALARM!"
    assert alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_triggers_during_day():
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    # During the day, it should produce the wrapped alarm's sound unchanged
    assert day_night_alarm.trigger() == "LOUD ALARM!"

def test_day_night_switched_alarm_triggers_at_night():
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=False)
    # At night, it should produce silence (an empty sound report)
    assert day_night_alarm.trigger() == ""

def test_day_night_switched_alarm_with_fake_alarm():
    wrapped_alarm = FakeAlarm("DISTINCT SOUND!")
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    # During the day, it should produce the wrapped alarm's sound unchanged
    assert day_night_alarm.trigger() == "DISTINCT SOUND!"

def test_hybrid_alarm_triggers_combined_sounds():
    alarm1 = LoudAlarm()
    alarm2 = LoudAlarm()
    hybrid_alarm = HybridAlarm([alarm1, alarm2])
    # Triggering it should produce the sounds of all member alarms combined
    # "LOUD ALARM! LOUD ALARM!"
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"

def test_hybrid_alarm_with_day_night_alarm():
    wrapped_alarm = LoudAlarm()
    day_night_alarm = DayNightSwitchedAlarm(wrapped_alarm, is_day=True)
    hybrid_alarm = HybridAlarm([day_night_alarm, LoudAlarm()])
    # Triggering it should produce "LOUD ALARM! LOUD ALARM!"
    assert hybrid_alarm.trigger() == "LOUD ALARM! LOUD ALARM!"