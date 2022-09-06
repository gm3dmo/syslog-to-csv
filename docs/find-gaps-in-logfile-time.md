## Finding time gaps
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

