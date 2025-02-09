.mode csv
select user_agent, count() as count_user_agent from gitrpcd group by user_agent order by count_user_agent desc;
