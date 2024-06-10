CREATE TABLE spokesd AS
    SELECT *
    FROM read_json_auto(['system-logs/split-logs-syslog/spokesd.json', 'system-logs/split-logs-syslog.1/spokesd.json' ], ignore_errors=True);
DESCRIBE spokesd;
