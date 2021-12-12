Instructions:

**Milestone 1**

1. export token
The code:
export BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAPYSVwEAAAAAlQz3JZp8dDAJGNrSNPkUSNws7ts%3DRdxEiF5HftFmX89Ud6JULz1nGUJJuEd0OXUGbD5jI4aBgu254E'

2. Read Tweets and write it to tweets.txt. 
The code:
python server.py

3. Read a tweet from a json file and write it to tweets.txt
The code:
python server.py --filename=temp.json

4. Compute frequencies of words and phrases. 
The code below would generate the frequency of the word important.
Example code:
python word_count.py --word=important

5. Compute the number of unique words.
The code:
python vocabulary_size.py

6. Access FAILURE.md
THe code:
gedit FAILURE.md 

**Milestone 2**

a. Read the SQL file and create the database

psql  
create database milestone2  
\q

psql milestone2 < schema_postgres.sql


b. 
- export token The code: export BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAPYSVwEAAAAAlQz3JZp8dDAJGNrSNPkUSNws7ts%3DRdxEiF5HftFmX89Ud6JULz1nGUJJuEd0OXUGbD5jI4aBgu254E'

- Read Tweets and write it to database. 
(need to run server_postgres.py for more than 2 min to get enough data for calculating the trendiness score)  
- Read Tweets and write it to database  
The code:
python server_postgres_test.py

- Read tweets from a json file and write it to database  
The code:
python server_postgres.py --filename=temp.json


c.Compute frequencies of words and phrases in the current minute
The code:
python word_count_postgres.py --phrase import_phrase

d.Compute the number of unique words in the current minute
python vocabulary_size_postgres.py 

e. Compute the trendiness of a phrase:
The code:
python trendiness_postgres.py --phrase import_phrase

- Note: For files that need access to database, you might need to modify "user" to align with your database username.
The code:
conn=psycopg2.connect("dbname=milestone2 user=gb760 password=123456 port=5432") 


