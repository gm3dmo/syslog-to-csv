.mode column
.headers on
SELECT 
      MIN(real_date) AS min_date, 
      MAX(real_date) AS max_date, 
      AGE(max_date, min_date) AS timespan
  FROM syslog;
