import argparse
import psycopg2

parser = argparse.ArgumentParser(description='word count')
parser.add_argument('--phrase',type=str)
args = parser.parse_args()

conn=psycopg2.connect("dbname=milestone2 user=gb760")  #, password="123456", host="localhost", port="5432"
cur=conn.cursor()

query = f'''
select log10((1+num_cur_min_p)/nullif((V_cur_min+ total_cur_min_num_phrase),0))-log10((1+num_prior_min_p)/ nullif((V_prior_min+total_prior_min_num_phrase),0)) as trendiness
from phrases p
inner join time t
on p.cur_time = t.cur_time 
where phrase = '{args.phrase}' 
order by p.cur_time desc
limit 1
'''
outcome = cur.execute(query)

conn.commit() 
cur.close()
conn.close()

# pinrt the outcome
if outcome == None:
    print("trendiness: 0")
else:
    print("trendiness:",outcome)
