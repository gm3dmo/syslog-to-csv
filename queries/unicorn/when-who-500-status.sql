
/* Extract users who had a 5xx error in unicorn. Broken down into timeframes */

.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', now) / 300 * 300, 'unixepoch')) AS timeframe,
       current_user,
       count(*) as count_of_user
FROM unicorn where status like '5%' 
GROUP BY timeframe 
ORDER BY timeframe;