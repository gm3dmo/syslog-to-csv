.mode csv
SELECT date_trunc('minute', "Timestamp") - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM "Timestamp") % 30) AS timeframe, 
  "exception.message", COUNT(*) AS total
  FROM hookshot 
  WHERE "exception.message" like '%Timeout exceeded while awaiting headers%' 
  GROUP BY timeframe, "exception.message" 
  ORDER BY timeframe;
