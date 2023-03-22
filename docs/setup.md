#### Install/Setup `syslog-to-csv`
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):

#### Run `syslog-to-csv.py`
To create a `syslog.csv` file in the working directory:

```
python3 syslog-to-csv.py /var/log/syslog
```

##### Use pypy for speed
If large files need to be processed more quickly then using [pypy3](https://www.pypy.org/) to replace python provides a very significant speed boost:

```
pypy3 syslog-to-csv.py /var/log/syslog.1
```

#### Extract from syslog
Some daemons don't have their own log file and write to the syslog file. These can be extracted using `syslog-daemon-splitter.py`:

```
pypy3 syslog-daemon-splitter.py system-logs/syslog
```

A directory named `split-logs-syslog` will be created and each daemon has it's own file there:

```
ls -l system-logs/split-logs-syslog --sort=size
total 32
-rw-r--r-- 1 dmo staff 795 Mar 21 21:38 babeld.log.csv
-rw-r--r-- 1 dmo staff 639 Feb 19 08:36 babeld.log
-rw-r--r-- 1 dmo staff 401 Feb 19 08:36 spokesd.log
-rw-r--r-- 1 dmo staff 307 Feb 19 08:36 gpgverify.log
-rw-r--r-- 1 dmo staff 288 Feb 19 08:36 systemd.log
-rw-r--r-- 1 dmo staff 281 Feb 19 08:36 hookshot-go.log
-rw-r--r-- 1 dmo staff 274 Feb 19 08:36 kernel.log
-rw-r--r-- 1 dmo staff 146 Feb 19 08:36 render.log
```

#### Install/Setup `kv-to-csv.py`
The `--log-type` arguement tells the script which log format we are processsing, in this case `babeld`:

```
kv-to-csv.py system-logs/split-logs-syslog/babeld.log --log-type babeld --csv-file system-logs/split-logs-syslog/babeld.log.csv
```
