import psycopg2

# create the connection
conn=psycopg2.connect("dbname=milestone2 user=gb760")  #, password="123456", host="localhost", port="5432"
cur=conn.cursor()

cur.execute('''
select phrase, cur_time, num_cur_min_p from phrases where len_word = 1 group by (phrase,cur_time)
''')
rs=cur.fetchall() 
for r in rs: print (r)

conn.commit() 
cur.close()
conn.close()
