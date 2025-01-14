WITH numbered_rows AS (
    SELECT
      daemon,
      line_number,
      real_date,
      line_number - ROW_NUMBER() OVER (ORDER BY line_number) AS grp
    FROM syslog
    WHERE daemon = 'kernel:'
  ),
  streak_lengths AS (
    SELECT
      daemon,
      grp,
      COUNT(*) as streak_length,
      MIN(line_number) as streak_start,
      MAX(line_number) as streak_end,
      MIN(real_date) as streak_start_time,
      MAX(real_date) as streak_end_time
    FROM numbered_rows
    GROUP BY daemon, grp
  )
  SELECT
    daemon,
    streak_length as longest_streak,
    streak_start as start_line,
    streak_end as end_line,
    streak_start_time,
    streak_end_time,
    AGE(streak_end_time, streak_start_time) as streak_duration
  FROM streak_lengths
  WHERE streak_length = (
    SELECT MAX(streak_length)
    FROM streak_lengths
  )
  ORDER BY streak_start;
