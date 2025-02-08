 SELECT
·     to_timestamp(floor(epoch(ts) / 300) * 300) AS five_min_bucket,
·     proto, msg,
·     COUNT(*) AS error_count
· FROM babeld
· WHERE lower(msg) LIKE '%error%'
· GROUP BY 1, 2, 3
