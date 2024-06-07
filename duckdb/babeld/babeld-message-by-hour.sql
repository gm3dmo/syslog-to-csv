.mode csv
.headers on
SELECT 
  DATE_TRUNC('hour', CAST(ts AS TIMESTAMP)) AS hour,
  msg,
  COUNT(*) AS msg_count
FROM babeld
GROUP BY hour, msg
ORDER BY hour;
