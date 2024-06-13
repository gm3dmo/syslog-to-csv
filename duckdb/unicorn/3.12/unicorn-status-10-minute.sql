.mode csv
.headers on
SELECT
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 10) AS timeframe,
SUM(CASE WHEN status LIKE '20%' THEN 1 ELSE 0 END) AS status_20x,
SUM(CASE WHEN status LIKE '30%' THEN 1 ELSE 0 END) AS status_30x,
SUM(CASE WHEN status = '403' THEN 1 ELSE 0 END) AS status_403,
SUM(CASE WHEN status = '404' THEN 1 ELSE 0 END) AS status_404,
SUM(CASE WHEN status = '406' THEN 1 ELSE 0 END) AS status_406,
SUM(CASE WHEN status = '409' THEN 1 ELSE 0 END) AS status_409,
SUM(CASE WHEN status = '422' THEN 1 ELSE 0 END) AS status_422,
SUM(CASE WHEN status LIKE '50%' THEN 1 ELSE 0 END) AS status_50x
FROM unicorn where Timestamp is not null
GROUP BY timeframe
ORDER BY timeframe;
