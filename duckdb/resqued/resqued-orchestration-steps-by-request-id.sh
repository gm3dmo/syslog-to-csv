read -p "Enter request ID: " REQUEST_ID

./duckdb bundle.db <<SQL
.mode csv
SELECT "Timestamp",
       "msg",
       "gh.repo.orchestration.step_name",
       "gh.repo.orchestration.state"
FROM resqued
WHERE   "gh.request_id" = '$REQUEST_ID';
SQL
