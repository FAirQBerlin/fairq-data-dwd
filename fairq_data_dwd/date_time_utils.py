from datetime import date, datetime, timedelta

from dateutil import relativedelta


def get_date_list(start_date: str, end_date: str = date.today().strftime("%Y-%m-%d")) -> list:
    """
    We need to request the brightsky api in year chunks because otherwise it is too slow. This function returns a list
    of tuples containing the dates for the api requests for a given timeframe. The start date gets the time 00:00:00,
    the end date 23:59:59 so the complete year is covered.
    :param start_date: first day for that the weather should be extracted, e.g. "2015-01-01"
    :param end_date: last day for that the weather should be extracted, e.g. "2015-01-01", default is today
    :return: list of tuples containing the dates for the api requests for a given timeframe
    """
    target_format_start_date = "%Y-%m-%d 00:00:00"
    target_format_end_date = "%Y-%m-%d 23:59:59"
    date_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    date_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    if (date_end_date - date_start_date).days >= 365:
        date_list = []
        updated_date = date_start_date
        while (updated_date + relativedelta.relativedelta(years=1)) <= date_end_date:
            date_list.append(
                (
                    updated_date.strftime(target_format_start_date),
                    (
                        updated_date + relativedelta.relativedelta(years=1) - relativedelta.relativedelta(days=1)
                    ).strftime(target_format_end_date),
                )
            )
            updated_date = updated_date + relativedelta.relativedelta(years=1)
        date_list.append(
            (updated_date.strftime(target_format_start_date), date_end_date.strftime(target_format_end_date))
        )
        return date_list
    else:
        return [(date_start_date.strftime(target_format_start_date), date_end_date.strftime(target_format_end_date))]


def get_forecast_start_date() -> str:
    """
    Get start date of forecast period (3 hours ago, so we include hours in the past for which we still only have a
    forecast and no observations).
    :return: start date of forecast period in correct string format
    """
    now = datetime.utcnow()
    date_start_date = now - relativedelta.relativedelta(hours=3)
    return date_start_date.strftime("%Y-%m-%dT%H:%M")


def get_forecast_end_date() -> str:
    """
    Get end date of forecast period (next 5 days).
    :return: end date of forecast period in correct string format
    """
    now = datetime.utcnow()
    date_end_date = now + relativedelta.relativedelta(days=5)
    date_end_date = date_end_date + relativedelta.relativedelta(hours=1)
    return date_end_date.strftime("%Y-%m-%dT%H:%M")


def two_days_ago():
    """
    Get date two days ago
    :return str: date formatted like "2022-07-01"
    """
    today = date.today()
    two_days = timedelta(days=2)
    day_two_days_ago = today - two_days
    return day_two_days_ago.strftime("%Y-%m-%d")
