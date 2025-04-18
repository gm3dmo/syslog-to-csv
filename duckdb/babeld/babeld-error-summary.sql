.mode csv
SELECT
    repo,
    SUBSTRING(msg, 1, 120) AS truncated_msg,
    COUNT(*) AS error_count
  FROM babeld
  WHERE
    log_level = 'ERROR'
    AND repo <> ''
    AND msg NOT LIKE 'sending response for status: No%'
  GROUP BY
    repo,
    SUBSTRING(msg, 1, 120)
  ORDER BY
    error_count DESC;

.mode column
SELECT
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
    repo,
    SUBSTRING(msg, 1, 120)
  ORDER BY
    error_count DESC;
  
