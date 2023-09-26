from datetime import datetime

from fairq_data_dwd.date_time_utils import get_date_list, get_forecast_end_date, get_forecast_start_date, two_days_ago


def test_get_date_list():
    # arrange
    start_end_date_list = [("2022-01-01", "2022-05-01"), ("2021-05-01", "2022-05-20"), ("2020-02-06", "2022-05-20")]

    # act
    res_list = [get_date_list(start_end_dates[0], start_end_dates[1]) for start_end_dates in start_end_date_list]

    # assert
    assert res_list[0] == [("2022-01-01 00:00:00", "2022-05-01 23:59:59")]
    assert res_list[1] == [
        ("2021-05-01 00:00:00", "2022-04-30 23:59:59"),
        ("2022-05-01 00:00:00", "2022-05-20 23:59:59"),
    ]
    assert res_list[2] == [
        ("2020-02-06 00:00:00", "2021-02-05 23:59:59"),
        ("2021-02-06 00:00:00", "2022-02-05 23:59:59"),
        ("2022-02-06 00:00:00", "2022-05-20 23:59:59"),
    ]


def test_get_forecast_end_date():
    # act
    res = get_forecast_end_date()

    # assert
    assert len(res) == 16
    assert res.startswith("20")
    assert datetime.strptime(res, "%Y-%m-%dT%H:%M") > datetime.now()


def test_get_forecast_start_date():
    # act
    res = get_forecast_start_date()

    # assert
    assert len(res) == 16
    assert res.startswith("20")
    assert datetime.strptime(res, "%Y-%m-%dT%H:%M") < datetime.now()


def test_two_days_ago():
    res = two_days_ago()
    assert res.startswith("20")
    assert len(res) == 10
