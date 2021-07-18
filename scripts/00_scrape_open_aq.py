import datetime
from time import sleep

import openaq

from summer_capstone.util.s3 import write_json_to_s3_object


def main():
    """Retrieve the last six months of Belgian air quality data and push to S3 as JSON"""

    start_date_string = "2021-03-01"
    start_date_from = datetime.datetime.strptime(start_date_string, "%Y-%m-%d").date()

    for i in range(0, 15):
        date_from = start_date_from + datetime.timedelta(i * 10)
        date_to = date_from + datetime.timedelta(days=(i + 1) * 10)
        params = {
            "date_from": date_from,
            "date_to": date_to,
            "limit": str(2),
            "country_id": "BE",
            "page": str(1)
        }
        api = openaq.OpenAQ(version="v2")
        response = api.measurements(**params)
        sleep(10)  # Avoid hammering the API
        s3_key = f"raw/open_aq/data_part_{i + 1}.json"
        write_json_to_s3_object(response[1]["results"], s3_key)


if __name__ == "__main__":
    main()
