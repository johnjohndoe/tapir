import datetime

cycle_start_dates = [
    datetime.date(year=2022, month=4, day=11),
]
cycle_start_dates.sort()

REMINDER_EMAIL_DAYS_BEFORE_SHIFT = 7

FREEZE_THRESHOLD = -4
FREEZE_AFTER_DAYS = 10
NB_WEEKS_IN_THE_FUTURE_FOR_MAKE_UP_SHIFTS = 8

FEATURE_FLAG_NAME_FROZEN_MEMBERS = "feature_flags.shifts.frozen_members"
