.mode csv
SELECT
  to_timestamp(floor(epoch("time") / 300) * 300) AS five_min_bucket,
  user_agent,
  COUNT(*) AS total_count
FROM gitrpcd
GROUP BY 1, 2
ORDER BY 1, 2;
