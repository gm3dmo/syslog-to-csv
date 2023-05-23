.mode csv
.headers on
SELECT strftime('%Y-%m-%dT%H:%M:%S', datetime(strftime('%s', now) / 300 * 300, 'unixepoch')) AS timeframe,
      sum(case when message = 'Authentication success via token' then 1 else 0 end) as auth_success_via_token,
      sum(case when message = 'Authentication failure via token' then 1 else 0 end) as auth_failure_via_token,
      sum(case when message = 'Your account has been suspended. via token' then 1 else 0 end) as account_suspended_via_token,
      sum(case when message = 'Authentication success' then 1 else 0 end) as auth_success,
      sum(case when message = 'Authentication failure' then 1 else 0 end) as auth_failure,
      sum(case when message = 'Password authentication is not supported by SAML authentication' then 1 else 0 end) as passwd_auth_not_supported_by_saml,
      sum(case when message like 'Unable to create the user because username is too long%' then 1 else 0 end) as username_too_long,
      SUM(case when message like 'The external%' then 1 else 0 end) as external_auth_server_failed_to_respond,
      SUM(case when message = 'Invalid LDAP login credentials.' then 1 else 0 end) as invalid_ldap_login_creds
FROM auth 
GROUP BY timeframe 
ORDER BY timeframe asc;
