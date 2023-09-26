from pytest import raises

from fairq_data_dwd.get_dwd_data import extract_dict_from_api_output, get_grid_coordinates, get_obs_of_valid_type


def test_get_grid_coordinates():
    # arrange
    expected_res = [
        (2.01, 1.0),
        (2.01, 1.01),
        (2.01, 1.02),
        (2.01, 1.03),
        (2.01, 1.04),
        (2.01, 1.05),
        (2.02, 1.0),
        (2.02, 1.01),
        (2.02, 1.02),
        (2.02, 1.03),
        (2.02, 1.04),
        (2.02, 1.05),
        (2.03, 1.0),
        (2.03, 1.01),
        (2.03, 1.02),
        (2.03, 1.03),
        (2.03, 1.04),
        (2.03, 1.05),
        (2.04, 1.0),
        (2.04, 1.01),
        (2.04, 1.02),
        (2.04, 1.03),
        (2.04, 1.04),
        (2.04, 1.05),
    ]

    # act
    res = get_grid_coordinates(lat_min=2.01, lat_max=2.04, lon_min=1.00, lon_max=1.05, step_size=0.01)
    # assert
    assert res == expected_res


def test_extract_dict_from_api_output():
    # arrange
    coordinates = (52.0, 13.0)
    hour_entry = {
        "cloud_cover": 100,
        "condition": "dry",
        "dew_point": 0.0,
        "fallback_source_ids": {
            "cloud_cover": 6963,
            "pressure_msl": 6963,
            "visibility": 6963,
            "wind_direction": 6963,
            "wind_gust_speed": 6963,
            "wind_speed": 6963,
        },
        "icon": "cloudy",
        "precipitation": 0.0,
        "pressure_msl": 1016.1,
        "relative_humidity": 91,
        "source_id": 46604,
        "sunshine": None,
        "temperature": 1.3,
        "timestamp": "2015-12-31T00:00:00+00:00",
        "visibility": 13820,
        "wind_direction": 160,
        "wind_gust_direction": None,
        "wind_gust_speed": 46.8,
        "wind_speed": 25.2,
    }
    expected_res = {
        "date_time": "2015-12-31 00:00:00",
        "lat": 52.0,
        "lon": 13.0,
        "wind_direction": 160,
        "precipitation": 0.0,
        "temperature": 1.3,
        "relative_humidity": 91,
        "cloud_cover": 100,
        "pressure_msl": 1016.1,
        "sunshine": None,
        "wind_speed": 25.2,
    }
    # act
    res = extract_dict_from_api_output(coordinates, hour_entry)
    # assert
    assert res == expected_res


def test_get_obs_of_valid_type():
    # arrange
    req = {
        "weather": [
            {"source_id": 1, "some_var": 10.1},
            {"source_id": 99, "some_var": 3.5},
            {"source_id": 7, "some_var": 4.0},
            {"source_id": 15, "some_var": 1.1},  # source ID not defined in sources; should never happen but who knows
        ],
        "sources": [
            {"id": 1, "observation_type": "forecast"},
            {"id": 99, "observation_type": "current"},
            {"id": 7, "observation_type": "historical"},
            {"id": 5, "observation_type": "something_else"},
        ],
    }

    expected_forecast = [{"source_id": 1, "some_var": 10.1}]
    expected_obs = [{"source_id": 99, "some_var": 3.5}, {"source_id": 7, "some_var": 4.0}]

    # act
    res_forecast = get_obs_of_valid_type("forecast", req)
    res_obs = get_obs_of_valid_type("observed", req)

    # assert
    assert expected_forecast == res_forecast
    assert expected_obs == res_obs


def test_get_obs_of_valid_type_error():
    with raises(ValueError, match="Allowed observation_types are: observed, forecast"):
        get_obs_of_valid_type("something_else", {})
