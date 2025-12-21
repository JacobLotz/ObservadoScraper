import calendar
import datetime

from scripts.migrationtrendfun import get_end_dates, get_month_end, get_start_dates


def test_GetMonthEnd():
    assert get_month_end(datetime.date(2024, 1, 15)) == 31
    assert get_month_end(datetime.date(2024, 2, 1)) == 29  # Leap year
    assert get_month_end(datetime.date(2023, 2, 1)) == 28
    assert get_month_end(datetime.date(2024, 4, 1)) == 30


def test_GetStartDates():
    result = get_start_dates(1, 1, 2024)
    expected = [
        datetime.date(2024, 1, 1),
        datetime.date(2024, 1, 11),
        datetime.date(2024, 1, 21),
    ]
    assert result == expected


def test_GetEndDates():
    result = get_end_dates(1, 1, 2024)
    expected = [
        datetime.date(2024, 1, 11),
        datetime.date(2024, 1, 21),
        datetime.date(2024, 1, 31),
    ]
    assert result == expected
