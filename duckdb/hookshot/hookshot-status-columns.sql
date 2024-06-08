.mode csv
.headers on
SELECT 
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 5) AS timeframe,
  COUNT(*) FILTER (WHERE status like '20%') AS '20x_status',
  COUNT(*) FILTER (WHERE status like '30%') AS '30x_status',
  COUNT(*) FILTER (WHERE status like '40%') AS '40x_status',
  COUNT(*) FILTER (WHERE status like '50%') AS '50x_status'
FROM hookshot
WHERE status != ''
GROUP BY timeframe
ORDER BY timeframe;
