.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', created_at) / 300 * 300, 'unixepoch')) AS timeframe,
       app,
       count(*) as count_of_app
FROM exceptions 
GROUP BY timeframe, app
ORDER BY timeframe, count_of_app desc;