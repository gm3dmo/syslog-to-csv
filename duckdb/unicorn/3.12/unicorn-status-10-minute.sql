.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:00:00', CAST(now AS TIMESTAMP)) AS timeframe,
         SUM(CASE WHEN status LIKE '20%' THEN 1 ELSE 0 END) AS status_20x,
         SUM(CASE WHEN status LIKE '30%' THEN 1 ELSE 0 END) AS status_30x,
         SUM(CASE WHEN status = '403' THEN 1 ELSE 0 END) AS status_403,
         SUM(CASE WHEN status = '404' THEN 1 ELSE 0 END) AS status_404,
         SUM(CASE WHEN status = '406' THEN 1 ELSE 0 END) AS status_406,
         SUM(CASE WHEN status = '409' THEN 1 ELSE 0 END) AS status_409,
         SUM(CASE WHEN status = '422' THEN 1 ELSE 0 END) AS status_422,
         SUM(CASE WHEN status LIKE '50%' THEN 1 ELSE 0 END) AS status_50x
  FROM unicorn
  GROUP BY timeframe
  ORDER BY timeframe;
