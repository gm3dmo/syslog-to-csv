 SELECT 
   app, 
   strftime('%Y-%m-%d %H:00:00', CAST(created_at AS TIMESTAMP)) AS hour, 
   COUNT(*) AS exception_count, message
FROM exceptions
GROUP BY app, message, hour
ORDER BY app, hour;
