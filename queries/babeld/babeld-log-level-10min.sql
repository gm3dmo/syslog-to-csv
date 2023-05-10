.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', ts) / 600 * 600, 'unixepoch')) AS bucket,
      sum(case when log_level = 'INFO' then 1 else 0 end) as info,
      sum(case when log_level = 'WARN' then 1 else 0 end) as error,
      sum(case when log_level = 'ERROR' then 1 else 0 end) as warn
FROM babeld GROUP BY bucket ORDER BY bucket ASC;
