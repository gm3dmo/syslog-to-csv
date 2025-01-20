.mode csv
.headers on
SELECT 
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 5) AS timeframe,
  "exception.message",
  COUNT(*) AS count
FROM hookshot where "exception.message" is not null
GROUP BY timeframe, "exception.message"
ORDER BY timeframe, "exception.message";
