CREATE TABLE hookshot AS
    SELECT *
    FROM read_json_auto(['system-logs/split-logs-syslog/hookshot-go.json', 'system-logs/split-logs-syslog.1/hookshot-go.json' ], ignore_errors=True);
     SELECT * FROM 'syslog-to-csv/hookshot-go.csv';

DESCRIBE hookshot;
