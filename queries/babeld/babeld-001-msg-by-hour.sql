.mode csv
.width 20 20 20 20
.headers on
.timer on
SELECT strftime('%Y-%m-%d %H:00:00', ts) as timeframe, 
      sum(case when msg like 'pubkey probe denied%' then 1 else 0 end) as pubkey_probe_denied,
      sum(case when msg like 'http op done: (-1)%%' then 1 else 0 end) as http_op_done_minus1,
      sum(case when msg like 'failed to verify pubkey:%' then 1 else 0 end) as pubkey_failed_verify,
      sum(case when msg like 'repo auth check failed:%' then 1 else 0 end) as repo_auth_check_failed,
      sum(case when msg like 'denying auth for non-git user%' then 1 else 0 end) as deny_auth_non_git_user,
      sum(case when msg like 'http op done: (403)%' then 1 else 0 end) as http_op_done_403,
      sum(case when msg like 'Timed out reading request body from client%' then 1 else 0 end) as tmout_read_req_body_from_client
FROM babeld GROUP BY timeframe ORDER BY timeframe;
