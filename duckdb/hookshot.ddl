.timer on
CREATE TABLE hookshot AS
     SELECT * FROM 'syslog-to-csv/hookshot-go.csv';

DESCRIBE hookshot;
