from django.test import TestCase
from pandas import DataFrame
import json
import sys

sys.path.append("./forecast")
from forecast.openWeather.api import get_weather_data, \
            OPENWEATHER_API_KEY
from forecast.openWeather.data_processing import create_forecast_entry, \
            create_forecast_df, calculate_daily_forecasts

TEST_LOCATION = (61.5, 23.8)

class OpenWeatherAPITests(TestCase):

    def test_api_key_exists(self):
        self.assertIsNotNone(OPENWEATHER_API_KEY)

    def test_api_key_format(self):
        if OPENWEATHER_API_KEY:
            self.assertRegex(OPENWEATHER_API_KEY, r"[a-z0-9]{32}")

    def test_get_weather_data(self):
        response = get_weather_data(
            TEST_LOCATION[0], 
            TEST_LOCATION[1])
        self.assertNotEqual(response, {})
        with open("forecast/test/logs/api_response.json", 'w') as f:
            f.write(json.dumps(response))
            f.close()

SAMPLES_FOLDER = "forecast/tests/samples"
SINGLE_FORECAST_TEST = "single_forecast"
MULTIPLE_FORECASTS_TEST = "multiple_forecasts"
DAILY_FORECAST_TEST = "daily_forecast"

def load_json_test_pair(name)->tuple:

    input_file = f"{SAMPLES_FOLDER}/{name}_in.json" 
    output_file = f"{SAMPLES_FOLDER}/{name}_out.json" 
    
    try:
        with open(input_file, "r") as f:
            input_data = json.loads(f.read())
            f.close()
    except Exception as e:
        print("Error reading the input file")
        print(e)
        return (dict(), dict())

    try:
        with open(output_file, "r") as f:
            output_data = json.loads(f.read())
            f.close()
    except Exception as e:
        print("Error reading the output file")
        print(e)
        return (dict(), dict())
    
    return (input_data, output_data)

class DataProcessingTests(TestCase):    

    def test_create_forecast_entry(self):
        input_data, output_data = load_json_test_pair(SINGLE_FORECAST_TEST)
        self.assertEqual(create_forecast_entry(input_data), output_data)

    def test_create_forecast_df(self):
        input_data, output_data = load_json_test_pair(MULTIPLE_FORECASTS_TEST)
        test_df = create_forecast_df(input_data)
        valid_df = DataFrame(output_data)
        self.assertTrue(test_df.equals(valid_df))
    
    def test_calculate_daily_forecasts(self):
        input_data, output_data = load_json_test_pair(DAILY_FORECAST_TEST)
        test_forecasts = calculate_daily_forecasts(input_data)
        self.assertEqual(test_forecasts, output_data)