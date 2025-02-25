SELECT b.repo,
       g."gh.auth.login",
       g."gh.auth.hashed_token",
       COUNT(*) AS repo_access_count
FROM gitauth g
JOIN babeld b ON b.id = g."gh.request_id"
WHERE g."gh.auth.login" <> ''
GROUP BY b.repo, g."gh.auth.login", g."gh.auth.hashed_token"
ORDER BY repo_access_count DESC limit 10;
