from calcduedate import CalcDueDate

DATES_TIMES = [
    {'date': '2019-12-05 12:00:00', 'turnaround': 16},
    {'date': '2019-12-06 16:59:59', 'turnaround': 1},
    {'date': '2019-12-03 14:00:00', 'turnaround': 28},
]

calcduedate = CalcDueDate()
for dates_times in DATES_TIMES:
    calcduedate.calculate(submit_datetime=dates_times['date'],
                          turnaround_time=dates_times['turnaround'])
    print(calcduedate.issue_resolved)
