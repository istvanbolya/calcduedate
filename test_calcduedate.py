import datetime
from unittest import TestCase

from calcduedate import CalcDueDate, CalcDueDateException


class CalcDueDateTest(TestCase):

    def setUp(self):
        self.calcduedate = CalcDueDate()

    def test_validate_datetime_format(self):
        date1 = '2019-12-05 12:00:00'
        formatted_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 12,
            'minute': 0,
            'second': 0}
        formatted_datetime = datetime.datetime(**formatted_datetime_values)
        self.calcduedate._validate_datetime_format(date1)
        self.assertEqual(self.calcduedate.submit_datetime, formatted_datetime)
        date2 = '2019/12/05 12:00:00'
        with self.assertRaises(CalcDueDateException) as context:
            self.calcduedate._validate_datetime_format(date2)
        self.assertTrue('Date is not in valid format' in str(context.exception))
        date3 = 2019
        with self.assertRaises(CalcDueDateException) as context:
            self.calcduedate._validate_datetime_format(date3)
        self.assertTrue('Date is not in valid format' in str(context.exception))

    def test_validate_working_hours(self):
        submit_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 12,
            'minute': 0,
            'second': 0}
        self.calcduedate.submit_datetime = datetime.datetime(**submit_datetime_values)
        self.assertIsNone(self.calcduedate._validate_working_hours())
        submit_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 8,
            'minute': 0,
            'second': 0}
        self.calcduedate.submit_datetime = datetime.datetime(**submit_datetime_values)
        with self.assertRaises(CalcDueDateException) as context:
            self.calcduedate._validate_working_hours()
        self.assertTrue('Issue is submitted outside of working hours' in str(context.exception))

    def test_set_days_hours_to_resolve(self):
        turnaround_time = 16
        self.calcduedate._set_days_hours_to_resolve(turnaround_time)
        self.assertEqual(self.calcduedate.workdays_to_resolve, 2)
        self.assertEqual(self.calcduedate.workhours_to_resolve, 0)
        turnaround_time = 0
        self.calcduedate._set_days_hours_to_resolve(turnaround_time)
        self.assertEqual(self.calcduedate.workdays_to_resolve, 0)
        self.assertEqual(self.calcduedate.workhours_to_resolve, 0)
        turnaround_time = 49
        self.calcduedate._set_days_hours_to_resolve(turnaround_time)
        self.assertEqual(self.calcduedate.workdays_to_resolve, 6)
        self.assertEqual(self.calcduedate.workhours_to_resolve, 1)
        turnaround_time = 7
        self.calcduedate._set_days_hours_to_resolve(turnaround_time)
        self.assertEqual(self.calcduedate.workdays_to_resolve, 0)
        self.assertEqual(self.calcduedate.workhours_to_resolve, 7)
        turnaround_time = '16'
        with self.assertRaises(CalcDueDateException) as context:
            self.calcduedate._set_days_hours_to_resolve(turnaround_time)
        self.assertTrue('Cannot get days and hours for resolve' in str(context.exception))

    def test_increase_resolve_hours(self):
        submit_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 12,
            'minute': 0,
            'second': 0}
        self.calcduedate.submit_datetime = datetime.datetime(**submit_datetime_values)

        self.calcduedate.workdays_to_resolve = 1
        self.calcduedate.workhours_to_resolve = 7
        self.calcduedate._increase_resolve_hours()
        self.assertEqual(self.calcduedate.workdays_to_resolve, 2)
        self.assertEqual(self.calcduedate.hour_for_resolve, 11)

        self.calcduedate.workdays_to_resolve = 1
        self.calcduedate.workhours_to_resolve = 4
        self.calcduedate._increase_resolve_hours()
        self.assertEqual(self.calcduedate.workdays_to_resolve, 1)
        self.assertEqual(self.calcduedate.hour_for_resolve, 16)

    def test_increase_resolve_days(self):
        submit_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 12,
            'minute': 0,
            'second': 0}
        self.calcduedate.submit_datetime = datetime.datetime(**submit_datetime_values)

        self.calcduedate.workdays_to_resolve = 11
        self.calcduedate._increase_resolve_days()
        self.assertEqual(self.calcduedate.workdays_to_resolve, 15)

        self.calcduedate.workdays_to_resolve = 1
        self.calcduedate._increase_resolve_days()
        self.assertEqual(self.calcduedate.workdays_to_resolve, 1)

        self.calcduedate.workdays_to_resolve = 4
        self.calcduedate._increase_resolve_days()
        self.assertEqual(self.calcduedate.workdays_to_resolve, 6)

    def test_set_resolve_date(self):
        submit_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 12,
            'minute': 0,
            'second': 0}
        self.calcduedate.submit_datetime = datetime.datetime(**submit_datetime_values)

        self.calcduedate.workdays_to_resolve = 6
        self.calcduedate.hour_for_resolve = 12
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 11,
            'hour': 12,
            'minute': 0,
            'second': 0}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)

        self.calcduedate._set_resolve_datetime()
        self.assertEqual(self.calcduedate.issue_resolved, resolve_datetime)

        self.calcduedate.workdays_to_resolve = 0
        self.calcduedate.hour_for_resolve = 12
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 12,
            'minute': 0,
            'second': 0}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)

        self.calcduedate._set_resolve_datetime()
        self.assertEqual(self.calcduedate.issue_resolved, resolve_datetime)

        submit_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 5,
            'hour': 16,
            'minute': 59,
            'second': 59}
        self.calcduedate.submit_datetime = datetime.datetime(**submit_datetime_values)

        self.calcduedate.workdays_to_resolve = 2
        self.calcduedate.hour_for_resolve = 9
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 7,
            'hour': 9,
            'minute': 59,
            'second': 59}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)

        self.calcduedate._set_resolve_datetime()
        self.assertEqual(self.calcduedate.issue_resolved, resolve_datetime)

    def test_calculate(self):
        calc_params = {
            'submit_datetime': '2019-12-05 12:00:00',
            'turnaround_time': 16
        }
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 9,
            'hour': 12,
            'minute': 0,
            'second': 0}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)
        resolve_datetime_calculated = self.calcduedate.calculate(**calc_params)
        self.assertEqual(resolve_datetime_calculated, resolve_datetime)

        calc_params = {
            'submit_datetime': '2019-12-06 16:59:59',
            'turnaround_time': 1
        }
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 9,
            'hour': 9,
            'minute': 59,
            'second': 59}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)
        resolve_datetime_calculated = self.calcduedate.calculate(**calc_params)
        self.assertEqual(resolve_datetime_calculated, resolve_datetime)

        calc_params = {
            'submit_datetime': '2019-12-05 16:59:59',
            'turnaround_time': 1
        }
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 6,
            'hour': 9,
            'minute': 59,
            'second': 59}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)
        resolve_datetime_calculated = self.calcduedate.calculate(**calc_params)
        self.assertEqual(resolve_datetime_calculated, resolve_datetime)

        calc_params = {
            'submit_datetime': '2019-12-05 16:59:59',
            'turnaround_time': 9
        }
        resolve_datetime_values = {
            'year': 2019,
            'month': 12,
            'day': 9,
            'hour': 9,
            'minute': 59,
            'second': 59}
        resolve_datetime = datetime.datetime(**resolve_datetime_values)
        resolve_datetime_calculated = self.calcduedate.calculate(**calc_params)
        self.assertEqual(resolve_datetime_calculated, resolve_datetime)
