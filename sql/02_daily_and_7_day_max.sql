-- Compare on a daily basis the maximum value of an air quality parameter to the maximum value that that parameter
-- had over the last 7 days.
with temp as (
 select
    date(utc) as dt,
    parameter,
    max(value) as daily_max
 from AQ
 group by date(utc), parameter
 )
select
    dt,
     parameter,
     daily_max,
     max(daily_max) over (
        partition by dt, parameter
        order by dt desc
        rows between 6 PRECEDING and CURRENT ROW
     ) as "7_days_max"
from temp order by parameter, dt;