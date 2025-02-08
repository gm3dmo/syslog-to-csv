SELECT
  to_timestamp(floor(epoch(real_date) / 300) * 300) AS five_min_bucket,
  daemon,
  COUNT(*) AS error_count
FROM syslog
WHERE lower(wiped_line) LIKE '%error%'
GROUP BY 1, 2
ORDER BY 1, 2;
