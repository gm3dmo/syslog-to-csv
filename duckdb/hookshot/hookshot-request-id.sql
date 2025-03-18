.mode columns
SELECT
     github_request_id,
     EXTRACT(EPOCH FROM MAX(Timestamp) - MIN(Timestamp)) AS time_difference_seconds
 FROM
     hookshot
 GROUP BY
     github_request_id
 ORDER BY
     time_difference_seconds DESC
LIMIT 20;
