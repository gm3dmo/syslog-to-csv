.mode column
SELECT 
    daemon,
    ROUND(AVG(line_length), 2) as avg_line_length,
    COUNT(*) as total_lines
FROM syslog 
GROUP BY daemon 
ORDER BY avg_line_length DESC;
