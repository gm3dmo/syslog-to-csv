.mode csv
.headers on
.timer on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', now) / 600 * 600, 'unixepoch')) AS timeframe,
SUM(case when message = 'Authentication success via token' then 1 else 0 end) as auth_success_via_token,
SUM(case when message = 'Your account has been suspended. via token' then 1 else 0 end) as account_suspended_via_token,
SUM(case when message = 'Authentication success' then 1 else 0 end) as auth_success,
SUM(case when message = 'Authentication failure' then 1 else 0 end) as auth_failure,
SUM(case when message = 'Authentication failure via token' then 1 else 0 end) as auth_failure_via_token,
SUM(case when message like 'The external%' then 1 else 0 end) as external_auth_server_failed_to_respond,
SUM(case when message = 'Invalid LDAP login credentials.' then 1 else 0 end) as invalid_ldap_login_creds
from auth
GROUP BY timeframe 
ORDER BY timeframe ASC;
