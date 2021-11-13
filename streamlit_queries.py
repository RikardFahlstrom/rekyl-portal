created_errands_per_date = """
select created_date, count(distinct rekyl_errand_id) from errands group by created_date order by 1;
"""

total_number_of_errands = """
select count(distinct rekyl_errand_id) from errands;
"""

top_reporter = """
select reporter, count(distinct rekyl_errand_id) as created_errands, max(created_date) as latest_errand from errands group by 1 order by 2 desc;
"""

created_errands_per_type = """
select created_date, errand_type, count(distinct rekyl_errand_id) as num_errands from errands group by 1,2;
"""

select_all = """
select * from errands;
"""
