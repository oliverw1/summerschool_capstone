import datetime
from typing import Union

import openaq

def query_open_aq(**kwargs) -> Union[dict, pd.DataFrame]:
    api = openaq.OpenAQ(version="v2")
    response = api.measurements(**kwargs)
    return response
