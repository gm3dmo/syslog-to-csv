.mode csv
.headers on
SELECT 
  DATE_TRUNC('hour', CAST("time" AS TIMESTAMP)) AS time_hour,
  "msg",
  COUNT(*) AS msg_count
FROM gitrpcd
GROUP BY time_hour, "msg"
ORDER BY time_hour;
