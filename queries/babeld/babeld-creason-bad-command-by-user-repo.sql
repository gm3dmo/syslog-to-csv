### Which users/repos/banner  are "bad command" messages coming from in the babeld.log?

.headers on
.mode column
.width 20 30 30 
select creason, user agent, repo, banner, count(creason) as count_of_bad_command from babeld 
where creason like 'bad command' 
group by creason, user_agent, repo 
order by count_of_bad_command desc 
limit 50;