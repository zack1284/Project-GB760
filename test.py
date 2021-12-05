#!/usr/bin/env python

import psycopg
import psycopg2


# open a connection (make sure to close it later)
#conn = psycopg.connect("dbname=abc user=gb760")
#conn = psycopg2.connect("dbname=abc user=gb760")

# create a cursor
#cur = conn.cursor()

def insert_vendor_list(vendor_list):
	""" insert multiple vendors into the vendors table  """
	sql = """INSERT INTO phrases(phrase,str_time) VALUES(%s,%s)"""
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect("dbname=abc user=gb760")
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.executemany(sql,vendor_list)
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
            
if __name__ == '__main__':
	""" insert multiple vendors into the vendors table  """
	sql = """INSERT INTO phrases(phrase,str_time) VALUES(%s,%s)"""
	conn = None
	try:
		# connect to the PostgreSQL database
		conn = psycopg2.connect("dbname=abc user=gb760")
		# create a new cursor
		cur = conn.cursor()
		# execute the INSERT statement
		cur.execute(sql,('asd','2021'))
		# commit the changes to the database
		conn.commit()
		# close communication with the database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
            
