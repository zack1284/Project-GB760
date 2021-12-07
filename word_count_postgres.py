import time
import psycopg2
import argparse

def now_local_time():
    now_time = str(time.strftime("%H-%M", time.localtime()))
    return(now_time)

def now_local_sec():
    now_sec = int(time.strftime("%S", time.localtime()))
    return(now_sec)

def main():
# create the connection
    now_time = now_local_time()
    now_sec = now_local_sec()

    # use arg parse to input data
    parser = argparse.ArgumentParser(description='word count')
    parser.add_argument('--phrase',type=str)
    args = parser.parse_args()

    # connect to database
    conn=psycopg2.connect("dbname=milestone2 user=gb760")  #user=postgre password="123456", host="localhost", port="5432"
    cur=conn.cursor()

    # write query to calculate
    query = f'''
    SELECT num_now_min_p
    FROM phrases
    WHERE phrase = '{args.phrase}' AND cur_time LIKE '%{now_time}%' and cur_sec <= {now_sec}
    '''

    outcome = cur.execute(query)

    conn.commit() 
    cur.close()
    conn.close()

    # pinrt the outcome
    if outcome == None:
        print(0)
    else:
        print(outcome)

if __name__ == "__main__":
    main()

