.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', time) / 600 * 600, 'unixepoch')) AS timeframe,
      sum(case when status like '20%' then 1 else 0 end) as status_20x,
      sum(case when status like '30%' then 1 else 0 end) as status_30x,
      sum(case when status = '403' then 1 else 0 end) as status_403,
      sum(case when status = '404' then 1 else 0 end) as status_404,
      sum(case when status = '406' then 1 else 0 end) as status_406,
      sum(case when status like '50%' then 1 else 0 end) as status_50x
FROM hookshot 
GROUP BY timeframe
ORDER BY timeframe ASC;
