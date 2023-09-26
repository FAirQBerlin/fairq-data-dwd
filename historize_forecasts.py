"""
This script queries dwd forecasts for the next 5 days and historizes them in the clickhouse db.
We need to run this script on a regular basis because the API does not return historical forecasts.
However, we need these to train and evaluate the model on forecasts instead of actual values,
because we won't know the actual weather values when making our forecasts.
This script is used in a kubernetes job.
"""

from datetime import datetime

from fairq_data_dwd.date_time_utils import get_forecast_end_date, get_forecast_start_date
from fairq_data_dwd.db_connect import send_data_clickhouse
from fairq_data_dwd.get_dwd_data import get_grid_coordinates, retrieve_data_from_api

coordinates_list = get_grid_coordinates()
end_date = get_forecast_end_date()
start_date = get_forecast_start_date()

df_for_db = retrieve_data_from_api(coordinates_list, start_date, end_date, "forecast")
date_time_forecast = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
df_for_db["date_time_forecast"] = date_time_forecast

print(f"Sending data for period: {start_date} until {end_date} to clickhouse.")
send_data_clickhouse(df_for_db, schema_name="fairq_raw", table_name="dwd_forecasts")
