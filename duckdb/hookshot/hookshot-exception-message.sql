SELECT
  date_trunc('minute', CAST("Timestamp" AS TIMESTAMP)) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM CAST("Timestamp" AS TIMESTAMP)) % 10) AS timeframe,
  "http.status_code", "gh.repo.name_with_owner", "gh.request.api.route",  COUNT(*) AS count
FROM unicorn
WHERE "http.status_code" > 299
GROUP BY timeframe, "gh.repo.name_with_owner", "http.status_code", "gh.request.api.route"
ORDER BY timeframe, "http.status_code";
