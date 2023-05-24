.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', now) / 300 * 300, 'unixepoch')) AS timeframe,
       current_user,
       count(*) as count_of_errors,
FROM unicorn where status like '5%' 
GROUP BY timeframe, route 
ORDER BY timeframe;

