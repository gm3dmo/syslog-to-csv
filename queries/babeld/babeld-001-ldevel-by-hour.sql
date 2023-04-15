.mode columns
.width 20 20 20 20
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', now) as hour, 
      sum(case when message = 'INFO' then 1 else 0 end) as info,
      sum(case when message = 'WARN' then 1 else 0 end) as error,
      sum(case when message = 'ERROR' then 1 else 0 end) as warn 
FROM babeld GROUP BY hour ORDER BY hour;
