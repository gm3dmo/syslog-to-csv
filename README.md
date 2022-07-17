## Turn log files into data

### Syslog to CSV
Convert a [syslog](https://tools.ietf.org/html/rfc5424) file to Comma Separated Values (CSV) format using [Python 3](https://python.org).  Tested with Debian 10 and AWS Linux but other syslog formats will probably work.

![syslog-to-csv](https://github.com/gm3dmo/syslog-to-csv/actions/workflows/syslog-to-csv.yml/badge.svg)


#### Install/Setup `syslog-to-csv`
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):

#### Run `syslog-to-csv.py`
To create a `syslog.csv` file in the working directory:

```
python3 syslog-to-csv.py /var/log/syslog
```

##### Use pypy for speed
If large files need to be processed more quickly then [pypy3](https://www.pypy.org/) can be used instead of python:

```
pypy3 syslog-to-csv.py /var/log/syslog.1
```

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

### Finding time gaps
Sometimes a virtual machine simply stops working for a period of time. To detect gaps in the log files time sequence `find-time-gaps.py` can be used.

#### find-time-gaps.py
This script has a dependency on pandas. Calling it like this:

```
python3 find-time-gaps.py -f syslog.csv real_date --gap 150 --output-format=markdown
```

Will return a markdown table indicating where the gap between two adjacent lines is 150 seconds or greater:

|   line_number |   time_difference | longer_gap   | line                                                            |
|--------------:|------------------:|:-------------|:----------------------------------------------------------------|
|          2170 |               172 | True         | Aug 15 08:32:53 debian anacron[438]: Job `cron.weekly' started  |
|          2196 |               173 | True         | Aug 15 08:37:53 debian anacron[438]: Job `cron.monthly' started |

### Tools for other file formats

- `kv-to-csv.py` process files with kv pairs to csv.
- `jsonl-to-csv.py` process files with json lines (jsonl) to csv.
- 
