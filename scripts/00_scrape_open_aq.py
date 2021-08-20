import datetime
from time import sleep

import openaq

from summer_capstone.util.s3 import write_json_to_s3_object


def main():
    """Retrieve the last six months of Belgian air quality data and push to S3 as JSON"""

    start_date_string = "2021-01-01"
    start_date_from = datetime.datetime.strptime(
        start_date_string, "%Y-%m-%d"
    ).date()

    for i in range(0, 60):
        date_from = start_date_from + datetime.timedelta(i * 3)
        date_to = date_from + datetime.timedelta(days=(i + 1) * 3)
        params = {
            "date_from": date_from,
            "date_to": date_to,
            "limit": str(10000),
            "country_id": "BE",
            "page": str(1),
            "parameter": ["pm10", "pm25", "pm1", "co"],
        }
        api = openaq.OpenAQ(version="v2")
        while True:
            try:
                response = api.measurements(**params)
                break
            except openaq.exceptions.ApiError as e:
                print(e)
                sleep(30)  # Avoid hammering the API
        s3_key = f"raw/open_aq/data_part_{i + 1}.json"
        write_json_to_s3_object(response[1]["results"], s3_key)
        print(i)


if __name__ == "__main__":
    main()
