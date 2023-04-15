.mode columns
.width 60
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', now) as hour, 
      sum(case when message = '' then 1 else 0 end) as column1,
      sum(case when message = '' then 1 else 0 end) as column2 
FROM babeld GROUP BY hour ORDER BY hour;
