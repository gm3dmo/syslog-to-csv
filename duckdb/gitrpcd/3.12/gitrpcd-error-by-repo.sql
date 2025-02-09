.mode csv
select repository_id, error, count() count_error from gitrpcd where error != '' group by repository_id, error order by count_error desc limit 20;
