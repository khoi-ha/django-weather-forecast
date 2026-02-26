import pandas as pd


def create_forecast_entry(json_entry:dict):
    """Create a forecast entry from a JSON response.

    Args:
        json_entry (dict): A dictionary containing weather data for a specific time.

    Returns:
        The data for a single forecast entry as a list.
    """
    row_data = []

    date, time = json_entry["dt_txt"].split(" ")
    precipitation = 0
    snowfall = 0
    
    if "rain" in json_entry.keys():
        precipitation = json_entry["rain"]["3h"]
    if "snow" in json_entry.keys():
        snowfall  = json_entry["snow"]["3h"]
    
    try:
        row_data = [
            date, time, 
            json_entry["main"]["temp_min"], 
            json_entry["main"]["temp_max"],
            json_entry["main"]["feels_like"],
            precipitation,
            snowfall,
            json_entry["clouds"]["all"],
            json_entry["wind"]["speed"]
        ]
    except KeyError:
        print("The given data is invalid")
        
    return row_data


def create_forecast_df(weather_data):
    """Create a DataFrame from the weather data.

    Args:
        weather_data (dict): The weather data returned from the API.

    Returns:
        pd.DataFrame: A DataFrame containing the forecast data.
    """
    rows = []
    forecast_entries = weather_data["list"]
    
    for entry in forecast_entries:
        row = create_forecast_entry(entry)
        rows.append(row)

    forecast_df = pd.DataFrame(rows, columns=["date", "time", "temp_min", "temp_max", "feels_like", 
                                            "precipitation", "snowfall", "cloud_cover", "wind_speed"])
    return forecast_df

def calculate_daily_forecasts(weather_data, days=3):
    """Calculate daily weather forecasts.

    Args:
        weather_data (dict): The weather data returned from the API.
        days (int, optional): The number of days to forecast. Defaults to 3.

    Returns:
        list: A list of dictionaries containing the daily forecast data.
    """
    grouped = create_forecast_df(weather_data).groupby("date")
    daily_forecasts = []
    for date, group in grouped:
        if len(daily_forecasts) >= days:
            break
        daily_forecast = {
            "date": date,
            "temp_min": round(float(group["temp_min"].min()),2),
            "temp_max": round(float(group["temp_max"].max()),2),
            "feels_like": round(float(group["feels_like"].mean()),2),
            "precipitation": round(float(group["precipitation"].sum()),2),
            "snowfall": round(float(group["snowfall"].sum()),2),
            "cloud_cover": round(float(group["cloud_cover"].mean()),2),
            "wind_speed": round(float(group["wind_speed"].mean()),2)
        }
        daily_forecasts.append(daily_forecast)
    return daily_forecasts
