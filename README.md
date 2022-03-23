### Syslog to CSV
Convert a [syslog](https://tools.ietf.org/html/rfc5424) file to Comma Separated Values (CSV) format using [Python 3](https://python.org)  This has been tested with Debian 10 and AWS Linux but other syslog formats will probably work.

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
If a line in the syslog input cannot be processed for some reason then an ERROR will be raised and the line will be skipped:

```
ERROR:syslog-to-csv:Could not parse: 2 (check resulted in Dispatch Password Requests to Console Directory Watch being skipped.)
ERROR:syslog-to-csv:squib: line 4 does not have host/daemon portion.
ERROR:syslog-to-csv:Could not parse: 9 (1900-00-30 07:03:29.68 line 4 runtime (CLR) functionality initialized.)
ERROR:syslog-to-csv:squib: line 10 is not minimum length of (15) characters
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
