import datetime


class CalcDueDateException(BaseException):
    pass


class CalcDueDate:

    DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_WORKING_HOUR_PER_DAY = 8
    DEFAULT_WORKING_HOUR_START = 9
    DEFAULT_WORKING_HOUR_END = DEFAULT_WORKING_HOUR_START + DEFAULT_WORKING_HOUR_PER_DAY

    def __init__(self):
        self.submit_datetime = None
        self.datetime_format = self.DEFAULT_DATETIME_FORMAT
        self.working_hour_per_day = self.DEFAULT_WORKING_HOUR_PER_DAY
        self.working_hours = [self.DEFAULT_WORKING_HOUR_START,
                              self.DEFAULT_WORKING_HOUR_START + self.DEFAULT_WORKING_HOUR_PER_DAY]
        self.workdays_to_resolve = None
        self.workhours_to_resolve = None
        self.hour_for_resolve = None
        self.issue_resolved = None

    def _validate_datetime_format(self, submit_datetime_str):
        try:
            self.submit_datetime = datetime.datetime.strptime(submit_datetime_str, self.datetime_format)
        except (ValueError, TypeError):
            raise CalcDueDateException('Date is not in valid format! Format: {}'.format(self.datetime_format))

    def _validate_working_hours(self):
        if self.submit_datetime.hour not in range(*self.working_hours):
            raise CalcDueDateException('Issue is submitted outside of working hours! Working hours: {}'.format(
                self.working_hours
            ))

    def _set_days_hours_to_resolve(self, turnaround_time):
        try:
            self.workdays_to_resolve = turnaround_time // self.working_hour_per_day
            self.workhours_to_resolve = turnaround_time % self.working_hour_per_day
        except TypeError:
            raise CalcDueDateException('Cannot get days and hours for resolve! Turnaround time: {}'.format(
                turnaround_time))

    def _increase_resolve_hours(self):
        issue_hour = self.submit_datetime.hour + self.workhours_to_resolve
        self.hour_for_resolve = issue_hour
        if issue_hour >= self.working_hours[1]:
            issue_diff = issue_hour - self.working_hours[1]
            self.workdays_to_resolve += 1
            self.hour_for_resolve = self.working_hours[0] + issue_diff

    def _increase_resolve_days(self):
        calculated_resolve_days = self.workdays_to_resolve
        submit_date = self.submit_datetime.date()
        current_day = 0
        while current_day < self.workdays_to_resolve:
            submit_date += datetime.timedelta(days=1)
            current_weekday = submit_date.weekday()
            if current_weekday == 5:
                calculated_resolve_days += 2
                current_day += 1
            current_day += 1
        self.workdays_to_resolve = calculated_resolve_days

    def _set_resolve_datetime(self):
        issue_resolved_values = {
            'days': self.workdays_to_resolve,
        }
        self.issue_resolved = (self.submit_datetime + datetime.timedelta(**issue_resolved_values))\
            .replace(hour=self.hour_for_resolve)

    def calculate(self, submit_datetime, turnaround_time):
        self._validate_datetime_format(submit_datetime)
        self._validate_working_hours()
        self._set_days_hours_to_resolve(turnaround_time)
        self._increase_resolve_hours()
        self._increase_resolve_days()
        self._set_resolve_datetime()
        return self.issue_resolved
