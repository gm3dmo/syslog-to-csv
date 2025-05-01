.timer on
CREATE TABLE resqued AS
     SELECT * FROM read_csv(['syslog-to-csv/resqued.1.csv', 'syslog-to-csv/resqued.csv' ]);

DESCRIBE resqued;
