
.mode csv
.headers on
SELECT 
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 5) AS timeframe,
  status,
  COUNT(*) AS count
FROM hookshot
GROUP BY timeframe, status
ORDER BY timeframe, status;
