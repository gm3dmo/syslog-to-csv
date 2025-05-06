.timer on
CREATE TABLE resqued AS
SELECT *
FROM read_csv_auto(
  ['syslog-to-csv/resqued.1.csv', 'syslog-to-csv/resqued.csv'],
  types={
    'gh.notifications.delivery.thread.id': 'VARCHAR'
  }
);
