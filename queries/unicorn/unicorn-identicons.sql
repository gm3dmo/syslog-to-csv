.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', now) / 3600 * 3600, 'unixepoch')) AS timeframe,
      sum(case when path_info  like '%identicons/app/oauth_app/85%' then 1 else 0 end) as path_info_85,
      status
FROM unicorn 
GROUP BY timeframe, status
ORDER BY timeframe ASC;