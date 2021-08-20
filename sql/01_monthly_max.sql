-- Show the maximum value of the air quality parameters (NOx, CO, ...) per month.
select month(date(utc)), parameter, max(value) as monthly_max from AQ
group by month(date(utc)),parameter;