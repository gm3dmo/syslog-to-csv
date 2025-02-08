.timer on
CREATE TABLE unicorn AS
     SELECT * FROM read_csv(['syslog-to-csv/github-unicorn.csv' ]);

DESCRIBE unicorn;
