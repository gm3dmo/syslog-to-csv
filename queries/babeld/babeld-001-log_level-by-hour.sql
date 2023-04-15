.mode columns
.width 20 20 20 20
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', ts) as hour, 
      sum(case when log_level = 'INFO' then 1 else 0 end) as info,
      sum(case when log_level = 'WARN' then 1 else 0 end) as error,
      sum(case when log_level = 'ERROR' then 1 else 0 end) as warn 
FROM babeld GROUP BY hour ORDER BY hour;
