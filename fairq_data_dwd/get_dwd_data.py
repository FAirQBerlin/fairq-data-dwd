import numpy as np
import pandas as pd
import requests
from dateutil import parser


def get_grid_coordinates(
    lat_min: float = 52.3, lat_max: float = 52.7, lon_min: float = 13.0, lon_max: float = 13.8, step_size: float = 0.05
) -> list:
    """
    Get list of coordinates from rectangle grid. The grid is defined by the min and max longitude and latitude values.
    Default values define a grid of Berlin coordinates.

    :param lat_min: minimum latitude value, defines the left border of the grid
    :param lat_max: maximum latitude value, defines the right border of the grid
    :param lon_min: minimum longitude value, defines the lower border of the grid
    :param lon_max: maximum longitude value, defines the upper border of the grid
    :param step_size: defines the distance between coordinates, default is 0.05 degrees (~ 5 km)
    :return: list of coordinates from rectangle grid in format [(lat, lon), ...]
    """
    berlin_grid_coordinates = []
    for x in np.arange(lat_min, lat_max, step_size):
        for y in np.arange(lon_min, lon_max, step_size):
            berlin_grid_coordinates.append((round(x, 2), round(y, 2)))
    return berlin_grid_coordinates


def extract_dict_from_api_output(coordinates: tuple, hour_entry: dict) -> dict:
    """
    Extract dict with relevant weather data for a given hour entry and coordination.
    :param coordinates: coordinates for which the weather data should be determined, e.g. (52.0, 13.0)
    :param hour_entry: dict from brightsky api containing weather data for given coordinates
    :return: dict with weather data
    """
    return {
        "date_time": parser.isoparse(hour_entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
        "lat": coordinates[0],
        "lon": coordinates[1],
        "wind_direction": hour_entry["wind_direction"],
        "wind_speed": hour_entry["wind_speed"],
        "precipitation": hour_entry["precipitation"],
        "temperature": hour_entry["temperature"],
        "relative_humidity": hour_entry["relative_humidity"],
        "cloud_cover": hour_entry["cloud_cover"],
        "pressure_msl": hour_entry["pressure_msl"],
        "sunshine": hour_entry["sunshine"],
    }


def retrieve_data_from_api(
    coordinates_list: list, start_date: str, end_date: str, observation_type: str
) -> pd.DataFrame:
    """
    Retrieve API Output for a given list of coordinates and time period, defined by start/end date.

    :param coordinates_list: list of coordinates from rectangle grid in format [(lat, lon), ...]
    :param start_date: start date as string in format "2022-06-16T17:27+02:00" (UTC + CE(S)T offset)
    :param end_date: end date as string in format "2022-06-16T17:27+02:00" (UTC + CE(S)T offset)
    :param observation_type: "observed" or "forecast", where "observed" includes both current and historical
    observations.
    This argument makes sure that only forecasts resp. observed value are extracted, depending on the objective.
    :return: pd.Dataframe containing dwd data for given coordinates and time period
    """
    dict_list = []
    print(f"Retrieving data for period: {start_date} until {end_date}")
    for coordinates in coordinates_list:
        r = requests.get(
            f"https://api.brightsky.dev/weather?date={start_date}&last_date={end_date}&lat={coordinates[0]}\
            + &lon={coordinates[1]}"
        )
        req = r.json()
        valid_weather_entries = get_obs_of_valid_type(observation_type, req)
        for hour_entry in valid_weather_entries:
            hour_dict = extract_dict_from_api_output(coordinates, hour_entry)
            dict_list.append(hour_dict)
    df = pd.DataFrame(dict_list)
    return df.replace(to_replace=np.nan, value=None)


def get_obs_of_valid_type(observation_type: str, api_response) -> list:
    """
    Keep only weather observations of the right type, i.e. "observed" or "forecast"
    :param observation_type: "observed" or "forecast"
    :param api_response: API response in json format
    :return: list of weather entries from the API of the valid type
    """
    if observation_type == "observed":
        allowed_types = ["current", "historical"]
    elif observation_type == "forecast":
        allowed_types = [observation_type]
    else:
        raise ValueError("Allowed observation_types are: observed, forecast")

    # Get the API-internal ID of the observation_type we want to extract
    valid_source_ids = [
        source["id"] for source in api_response["sources"] if source["observation_type"] in allowed_types
    ]
    valid_weather_entries = [entry for entry in api_response["weather"] if entry["source_id"] in valid_source_ids]
    return valid_weather_entries
