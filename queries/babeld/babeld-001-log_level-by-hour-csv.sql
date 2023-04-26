.mode csv
.headers on
SELECT strftime('%Y-%m-%d %H:00:00', ts) as timeframe, 
      sum(case when log_level = 'INFO' then 1 else 0 end) as info,
      sum(case when log_level = 'WARN' then 1 else 0 end) as error,
      sum(case when log_level = 'ERROR' then 1 else 0 end) as warn 
FROM babeld GROUP BY timeframe ORDER BY timeframe;
