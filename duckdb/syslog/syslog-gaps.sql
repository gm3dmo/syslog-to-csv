WITH time_gaps AS (
  SELECT 
    line_number,
    unix_timestamp,
    daemon,
    wiped_line,
    LAG(unix_timestamp) OVER (ORDER BY unix_timestamp) as prev_timestamp,
    LAG(line_number) OVER (ORDER BY unix_timestamp) as prev_line,
    LAG(daemon) OVER (ORDER BY unix_timestamp) as prev_daemon,
    LAG(wiped_line) OVER (ORDER BY unix_timestamp) as prev_message,
    unix_timestamp - LAG(unix_timestamp) OVER (ORDER BY unix_timestamp) as gap_seconds
  FROM syslog
  WHERE unix_timestamp IS NOT NULL
)
SELECT 
  prev_line as start_line,
  line_number as end_line,
  prev_daemon as start_daemon,
  daemon as end_daemon,
  gap_seconds,
  ROUND(gap_seconds/3600, 2) as gap_hours,
  to_timestamp(prev_timestamp) as start_time,
  to_timestamp(unix_timestamp) as end_time,
  prev_message as last_message_before_gap,
  wiped_line as first_message_after_gap
FROM time_gaps
WHERE gap_seconds IS NOT NULL
ORDER BY gap_seconds DESC
LIMIT 10;
