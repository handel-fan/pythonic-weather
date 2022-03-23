import requests
import json
from datetime import datetime
from pytz import timezone
from os.path import exists
import sys
import argparse

class OpenWeatherAPICall:
    """Make an API Call to OpenWeather!"""

    _open_weather_base_url = "https://api.openweathermap.org/data/2.5/onecall?"

    def open_weather_api_caller(self, api_key, location):
        try:
            response = requests.get(self._url_builder(api_key, location))

        except ConnectionError:
            print("Could not connect to server")
            sys.exit(1)

        if(response.status_code not in range(200, 299, 1)):
            print("unsuccessful get request")
            sys.exit(1)


        return response


    def _url_builder(self, api_key, location):
        latitude_string = "lat=" + self._get_latitude(location)

        longitude_string = "&lon=" + self._get_longitude(location)

        units_string = "&units=imperial"

        api_key_string = "&appid=" + api_key

        complete_url = self._open_weather_base_url + latitude_string + longitude_string + units_string + api_key_string

        return complete_url

    def _get_latitude(self, location):
        match location:
            case "Boston":
                return "42.36"

            case "San Francisco":
                return "37.77"

            case "London":
                return "51.50"

    def _get_longitude(self, location):
        match location:
            case "Boston":
                return "71.05"

            case "San Francisco":
                return "122.41"

            case "London":
                return "0.12"

class OpenWeatherJsonParser:
    """Parse the JSON from the API Call and put the useful information in an array!"""

    """Given a json string, put relevant information Bostoninto an array!"""
    def parse_json_to_csv_arr(self, response_json_string, location):
        csv_arr = [""] * 6
        open_weather_dictionary = json.loads(response_json_string)

        curr_timezone = self._get_timezone(location)
        curr_time = datetime.now(curr_timezone)

        csv_arr[0] = location
        csv_arr[1] = curr_time.strftime("%A %B %-d %Y")
        csv_arr[2] = str(open_weather_dictionary["current"]["temp"]) + "F"
        csv_arr[3] = open_weather_dictionary["current"]["weather"][0]["description"]
        csv_arr[4] = str(open_weather_dictionary["current"]["pressure"]) + "psi"
        csv_arr[5] = str(open_weather_dictionary["current"]["humidity"]) + "g.kg^(-1)"

        return csv_arr

    def _get_timezone(self, location):
        match location:
            case "Boston":
                return timezone("US/Eastern")
            case "San Francisco":
                return timezone("US/Pacific")
            case "London":
                return timezone("Europe/London")

class OpenWeatherFileIO:
    """Given a csv file path to output to, if the file already exists, append to it. If not, save to filepath if path is valid (directory that file is saved), throw errors if not."""


    """Work in progress! error checks like file validation will be added very soon. (pre-check whether valid directory, filenames without file extensions, etc.)"""
    def output_to_file(self, filepath, output_string):
        if(exists(filepath)):
            with open(filepath, "a") as append_file:
                append_file.write("\n\n")
                append_file.write(output_string)
        else:
            with open(filepath, "w") as write_file:
                write_file.write(output_string)

class PythonicWeatherRunner:
    """For each location, go from API Call to CSV array"""

    def api_to_csv_arr(api_key, location):
        api_response = OpenWeatherAPICall().open_weather_api_caller(api_key, location)
        json_string = json.dumps(api_response.json())
        return OpenWeatherJsonParser().parse_json_to_csv_arr(json_string, location)

    def csv_arr_to_csv_str(csv_arr, csv_str):
        for csv_elem in csv_arr:
            csv_str += csv_elem + ","

        return csv_str[:-1]


def main(api_key, file_out_path):

    csv_location_arr = ["Boston", "San Francisco", "London"]

    for location in csv_location_arr:
        csv_str = ""

        csv_arr = PythonicWeatherRunner.api_to_csv_arr(api_key, location)

        csv_str += PythonicWeatherRunner.csv_arr_to_csv_str(csv_arr, csv_str)

        OpenWeatherFileIO().output_to_file(file_out_path, csv_str)

if __name__ == "__main__":
    print("got here")
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("--api_key", help="Open Weather API Key")
    parser.add_argument("--csv_file_path", help="CSV File Path")
    args = parser.parse_args()
    print(args.api_key)
    print(args.csv_file_path)
    main(args.api_key, args.csv_file_path)

    # main("cd5053e95a6f10c7ce89187073e16930", "/home/jegan/pythonic-weather/dump1.csv")
