.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', ts) / 600 * 600, 'unixepoch')) AS timeframe,
      sum(case when creason = 'bad command' then 1 else 0 end) as creason_bad_command,
      sum(case when creason = 'drain ok' then 1 else 0 end) as creason_drain_ok,
      sum(case when creason = 'drain failed' then 1 else 0 end) as creason_drain_failed,
      sum(case when creason = 'git-lfs-authenticate command' then 1 else 0 end) as git_lfs_authenticate_command
FROM babeld
GROUP BY timeframe 
ORDER BY timeframe ASC;