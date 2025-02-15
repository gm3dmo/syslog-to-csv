.mode csv
SELECT
      daemon,
      COUNT(*) AS daemon_count,
      ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percent_of_total
  FROM syslog
  GROUP BY daemon
  ORDER BY daemon_count DESC;
