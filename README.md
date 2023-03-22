# Turn log files into data

## Table of Contents

1. [Setup Instructions](docs/setup.md)

- [Convert key value pairs (logfmt)](docs/key-value-pairs.md)
- [Convert jsonl format](docs/jsonl.md)
- [Find gaps in timestamps in a logfile](docs/find-gaps-in-logfile-time.md)

## Syslog to CSV and Key Value Pairs to CSV
Convert a [syslog](https://tools.ietf.org/html/rfc5424) file to Comma Separated Values (CSV) format using [Python 3](https://python.org).  Tested with Debian 10 and AWS Linux but other syslog formats will probably work. The `kv-to-csv.py` script will convert a file that is composed of lines of key value pairs to CSV.

![syslog-to-csv](https://github.com/gm3dmo/syslog-to-csv/actions/workflows/syslog-to-csv.yml/badge.svg)

The goal of the project is to be able to convert the most important (syslog, babeld, auth, unicorn) files from a GitHub Enterprise Server Support bundle to CSV for offline analysis.

##### Debug mode
Debug mode will print out details of each line as it is processed:

```
python3 -d syslog-to-csv.py /var/log/syslog
```


##### Skipped lines
If a line in the syslog input cannot be processed a WARNING is raised.The line is skipped:

```
WARNING:syslog-to-csv:Could not convert line number 150486 to utf-8: (b'Apr  1 20:33:22 testserver babeld[11452]: ts=2022-04-01T20:33:22.247904Z pid=1 tid=42 version=81d8f62 proto=ssh id=cb40592709493fa370ce6730da376af6 ip=23.95.222.129 srcp=43688 dstp=22 log_level=ERROR msg="ssh_handle_key_exchange failed: Protocol mismatch: \x16\x03\x01\x01\xfd\x01" conn_progress=0.4\n') 'utf-8' codec can't decode byte 0xfd in position 285: invalid start byte
```

##### Next Steps
With the data in CSV format a wide range of tools like Pandas, Sqlite or Excel can be used to interpret the syslog data. For example, this little chart was created using Pandas:

- Process the csv with [csvkit](https://csvkit.readthedocs.io/en/latest/) to get a summary of it's contents.


![Syslog Visualized](images/syslog-visualized.png)


