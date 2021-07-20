with dates as (SELECT DATEADD(day, Seq4(), date_from_parts(2021, 1, 1)) AS dt
FROM TABLE (Generator(rowcount => 180))),
date_param as (select dt, parameter from (select distinct parameter from AQ) cross join dates),
daily_max as (Select date(utc) as dt, parameter, max(value) as daily_max from AQ
             group by date(utc), parameter),
temp1 as (select date_param.parameter, date_param.dt, daily_max.daily_max from date_param left join daily_max on date_param.dt=daily_max.dt and date_param.parameter=daily_max.parameter
order by parameter, dt),
temp2 as (select *, lag(daily_max) ignore nulls over (partition by parameter order by dt asc) as previous_daily_max from temp1)
select parameter, dt, coalesce(daily_max, previous_daily_max) as daily_max from temp2
          order by parameter, dt;