select "gh.actor.login", count("gh.actor.login") as actor_login_count from unicorn group by "gh.actor.login" order by actor_login_count desc;
