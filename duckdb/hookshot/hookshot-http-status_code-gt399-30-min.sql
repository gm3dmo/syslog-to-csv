.mode csv
SELECT
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 30) AS timeframe,
  "http.status_code", "gh.repo.name_with_owner", hook_id,  COUNT(*) AS count
FROM unicorn
WHERE "http.status_code" > 399
GROUP BY timeframe, "gh.repo.name_with_owner", "http.status_code", "gh.request.api.route"
ORDER BY count, timeframe, "http.status_code";
