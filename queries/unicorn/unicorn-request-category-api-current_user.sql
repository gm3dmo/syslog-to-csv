
/* Extract "api" request category entries */

.mode csv
.timer on
.headers on

SELECT 
       strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', now) / 300 * 300, 'unixepoch')) AS timeframe,
       count(current_user) as count_of_current_user,
       current_user
FROM unicorn
WHERE request_category = "api"
GROUP BY timeframe
ORDER BY timeframe, count_of_current_user desc ;

