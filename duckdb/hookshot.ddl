.timer on
CREATE TABLE hookshot AS
     SELECT * FROM read_csv(['syslog-to-csv/hookshot-go.1.csv', 'syslog-to-csv/hookshot-go.csv' ]);

DESCRIBE hookshot;
