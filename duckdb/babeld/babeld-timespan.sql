.mode csv
.headers on
SELECT 
      MIN(CAST(ts AS TIMESTAMP)) AS min_date, 
      MAX(CAST(ts AS TIMESTAMP)) AS max_date, 
      AGE(MAX(CAST(ts AS TIMESTAMP)), MIN(CAST(ts AS TIMESTAMP))) AS timespan
  FROM babeld;
