.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', ts) / 300 * 300, 'unixepoch')) AS timeframe,
       user,
       count(*) as count_of_errors
FROM babeld WHERE log_level = 'ERROR' 
GROUP BY timeframe, user 
ORDER BY timeframe ASC;
