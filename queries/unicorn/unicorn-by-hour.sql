.mode columns
.width 20 20 20 20
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', now) as timeframe,
      sum(case when status like '20%' then 1 else 0 end) as status_20x,
      sum(case when status like '30%' then 1 else 0 end) as status_30x,
      sum(case when status = '403' then 1 else 0 end) as status_403,
      sum(case when status = '404' then 1 else 0 end) as status_404,
      sum(case when status = '406' then 1 else 0 end) as status_406,
      sum(case when status = '409' then 1 else 0 end) as status_409,
      sum(case when status = '422' then 1 else 0 end) as status_422,
      sum(case when status like '50%' then 1 else 0 end) as status_50x
FROM unicorn GROUP BY timeframe ORDER BY timeframe
