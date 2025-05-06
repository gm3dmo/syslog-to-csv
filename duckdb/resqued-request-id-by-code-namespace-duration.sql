.mode csv
SELECT
  "gh.request_id",
  "code.namespace",
  MIN("Timestamp") AS first_timestamp,
  MAX("Timestamp") AS last_timestamp,
  EXTRACT('epoch' FROM (MAX("Timestamp") - MIN("Timestamp"))) AS duration_seconds
FROM resqued
GROUP BY "gh.request_id", "code.namespace"
ORDER BY duration_seconds desc;
