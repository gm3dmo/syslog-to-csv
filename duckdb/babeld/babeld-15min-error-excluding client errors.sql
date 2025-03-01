SELECT
  -- 15-minute time bucket
  DATE_TRUNC('minute', ts)
    - (EXTRACT(MINUTE FROM ts) % 15) * INTERVAL '1' MINUTE AS time_bucket,
  repo,
  SUBSTRING(msg, 1, 120) AS truncated_msg,
  COUNT(*) AS error_count
FROM babeld
WHERE
  log_level = 'ERROR'
  AND repo <> ''
  AND msg NOT LIKE 'sending response for status: No%'
  AND msg NOT LIKE '%Invalid username or password%'
  AND msg NOT LIKE '%Repository not found%'
  AND msg NOT LIKE '%client write error%'
  AND msg NOT LIKE '%Your account is suspended%'
GROUP BY
  time_bucket,
  repo,
  truncated_msg
ORDER BY
  time_bucket DESC;
