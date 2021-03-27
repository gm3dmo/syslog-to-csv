# Syslog to CSV
Convert a [syslog](https://tools.ietf.org/html/rfc5424) file into a csv file (Debian 10) but others may work.

## syslog-to-csv
Download and unzip the [latest release](https://github.com/gm3dmo/syslog-to-csv/releases/latest):

Install the dependencies:

```
pip install -r requirements.txt
```

Run `syslog-to-csv.py`:

```
python syslog-to-csv.py /var/log/syslog.1
```
or if you need speed:

```
pypy syslog-to-csv.py /var/log/syslog.1
```
