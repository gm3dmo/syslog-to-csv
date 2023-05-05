.mode csv
.width 20 20 20 20
.headers on
.timer on
SELECT strftime('%Y-%m-%dT%H:00:00', now) as timeframe,
       current_user,
       count(*) as ct,
       elapsed
FROM unicorn where status like '5%' GROUP BY timeframe, route ORDER BY timeframe;
