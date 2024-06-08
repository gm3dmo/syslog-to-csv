.mode csv
.headers on
SELECT 
      MIN(CAST(Timestamp AS TIMESTAMP)) AS min_date, 
      MAX(CAST(Timestamp AS TIMESTAMP)) AS max_date, 
      AGE(MAX(CAST(Timestamp AS TIMESTAMP)), MIN(CAST(Timestamp AS TIMESTAMP))) AS timespan
  FROM unicorn;
