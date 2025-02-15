.mode csv
WITH intervals AS (
·     SELECT
·         -- Bucket timestamps into 5-minute intervals
·         DATE_TRUNC('minute', real_date)
·          - ((EXTRACT('minute' FROM real_date)::INTEGER % 5) * INTERVAL 1 minute)
·          AS interval_5m,
·         daemon,
·         COUNT(*) AS entries
·     FROM syslog
·     GROUP BY 1, 2
· ),
· ranked AS (
·     SELECT
·         intervals.*,
·         ROW_NUMBER() OVER (PARTITION BY interval_5m ORDER BY entries DESC) AS rn,
·         SUM(entries) OVER (PARTITION BY interval_5m) AS total_in_interval
·     FROM intervals
· )
· SELECT
·     interval_5m,
·     daemon,
·     entries,
·     ROUND(entries * 100.0 / total_in_interval, 2) AS percent_share
· FROM ranked
· WHERE rn <= 10
‣ ORDER BY interval_5m, entries DESC;
