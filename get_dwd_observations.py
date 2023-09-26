"""
This script queries the historic dwd data since a given date until today and writes it to the clickhouse db.
Default is the last 2 days to make sure that we don't have any gaps if the process does not run for a day.
This script is not used in any scheduled job anymore.
"""

import pandas as pd

from fairq_data_dwd.date_time_utils import get_date_list, two_days_ago
from fairq_data_dwd.db_connect import send_data_clickhouse
from fairq_data_dwd.get_dwd_data import get_grid_coordinates, retrieve_data_from_api

coordinates_list = get_grid_coordinates()
dates_list = get_date_list(start_date=two_days_ago())  # Change start_date to retrieve a specific time frame

df_list = []
for dates in dates_list:
    date_df = retrieve_data_from_api(coordinates_list, dates[0], dates[1], "observed")
    df_list.append(date_df)

df_for_db = pd.concat(df_list)
print(f"Sending data for period: {dates} to clickhouse.")
send_data_clickhouse(df_for_db, schema_name="fairq_raw", table_name="dwd_observations")
