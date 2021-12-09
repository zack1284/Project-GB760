import argparse
import psycopg2
import pandas as pd

parser = argparse.ArgumentParser(description='word count')
parser.add_argument('--phrase',type=str)
args = parser.parse_args()

conn = psycopg2.connect("dbname=milestone2 user=gb760")  #, password="123456", host="localhost", port="5432"
cur=conn.cursor()
sql = f'''
select log10((1+num_cur_min_p)/nullif((V_cur_min+ total_cur_min_num_phrase),0))-log10((1+num_prior_min_p)/ nullif((V_prior_min+total_prior_min_num_phrase),0)) as trendiness
from phrases p
full outer join time t
on p.cur_time = t.cur_time
where p.phrase = '{args.phrase}'
order by p.cur_time desc
limit 1
'''

conn.commit()
cur.close()
conn.close()

print(pd.read_sql(sql,conn))

# pinrt the outcome
