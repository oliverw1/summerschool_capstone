with temp as (Select date(utc) as dt, parameter, max(value) as daily_max from AQ
             group by date(utc), parameter)
select dt, parameter, daily_max, max(daily_max) over (partition by dt, parameter order by dt desc rows between 6 PRECEDING and CURRENT ROW) as "7_days_max"
from temp order by parameter, dt;