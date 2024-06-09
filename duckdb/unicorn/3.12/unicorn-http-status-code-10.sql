.mode csv
.headers on
SELECT 
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 10) AS timeframe,
  'http.status_code',
  COUNT(*) AS count
FROM unicorn 
GROUP BY timeframe, 'http.status_code'
ORDER BY timeframe, 'http.status_code';
