import spacy
import re
import io
from nltk import ngrams
import psycopg2

# clean the data again
open_file = open("tweet.txt")
file_tweet =open_file.read()

# clean the fata for counting
file_tweet = re.sub(r'@(\w+)','',file_tweet)
file_tweet_word = re.sub(r'[0-9]*','',file_tweet)
file_tweet_word = re.sub(r'[/]*','',file_tweet_word)
file_tweet_word = re.sub(r'[-]*','',file_tweet_word)
lines = file_tweet_word.splitlines()
#lines.remove('')

# list of unique cur_time
lines_time = file_tweet.splitlines()
lines_time.remove('')
words_in_line = []
for i in range(len(lines_time)):
  l = lines_time[i].split()
  words_in_line.append(l)
cur_time = []
for line in words_in_line:
  if line[0] in cur_time:
    continue
  else:
    cur_time.append(str(line[0]))
  
# split the unique time
# split the time
split_unique_time = []
split_time = []
for i in range(len(cur_time)):
  split_unique = cur_time[i].split('-')
  split_unique_time.append(split_unique)
for j in range(len(words_in_line)):
  date = words_in_line[j][0]
  split = date.split('-')
  split_time.append(split)


### get the variable lists in table 'Time'

# list of V_cur_min
# list of total_cur_min_num_phrase

V_cur_min = []
total_cur_min_num_phrase = []

for time_num in range(len(cur_time)):
  count_unique = 0
  count = 0
  unique_phrase = []
  for line_num in range(len(lines)):
    if split_time[line_num][2] != split_unique_time[time_num][2] or split_time[line_num][3] != split_unique_time[time_num][3] or split_time[line_num][4] != split_unique_time[time_num][4] or int(split_time[line_num][5]) < int(split_unique_time[time_num][5]):
      continue
    else:
      if lines[line_num] != ' ':
        bigrams1 = ngrams(lines[line_num].split(), 1)
        bigrams2 = ngrams(lines[line_num].split(), 2)
        for gram1 in bigrams1:
          count += 1
          if gram1 not in unique_phrase:
            unique_phrase.append(gram1)
            count_unique += 1
        for gram2 in bigrams2:
          count += 1
          if gram2 not in unique_phrase:
            unique_phrase.append(gram2)
            count_unique += 1
      else:
        count_unique += 0
        count += 0

  V_cur_min.append(count_unique)
  total_cur_min_num_phrase.append(count)

# list of V_prior_min
# list of total_prior_min_num_phrase

V_prior_min = []
total_prior_min_num_phrase = []

for time_num in range(len(cur_time)):
  count_unique = 0
  count = 0
  unique_phrase = []
  for line_num in range(len(lines)):
    if split_time[line_num][2] != split_unique_time[time_num][2] or split_time[line_num][3] != split_unique_time[time_num][3] or int(split_time[line_num][4]) + 1 != int(split_unique_time[time_num][4]):
      continue
    else:
      if lines[line_num] != ' ':
        bigrams1 = ngrams(lines[line_num].split(), 1)
        bigrams2 = ngrams(lines[line_num].split(), 2)
        for gram1 in bigrams1:
          count += 1
          if gram1 not in unique_phrase:
            unique_phrase.append(gram1)
            count_unique += 1
        for gram2 in bigrams2:
          count += 1
          if gram2 not in unique_phrase:
            unique_phrase.append(gram2)
            count_unique += 1
      else:
        count_unique += 0
        count += 0

  V_prior_min.append(count_unique)
  total_prior_min_num_phrase.append(count)


### get the list of variables in the table 'Phrases'

# list of unique sets of phrase and time
phrase = []
for line_num in range(len(lines)):
  if lines[line_num] != ' ':
    bigrams1 = ngrams(lines[line_num].split(), 1)
    bigrams2 = ngrams(lines[line_num].split(), 2)
    for gram1 in bigrams1:
      set_ = [str(words_in_line[line_num][0]), str(gram1[0])]
      if set_ not in phrase:
        phrase.append(set_)
    for gram2 in bigrams2:
      set_ = [str(words_in_line[line_num][0]), str(gram2[0] + ' ' + gram2[1])]
      if set_ not in phrase:
        phrase.append(set_)
  else:
    continue

# split the time in each phrase set
split_set_time = []
for i in range(len(phrase)):
  split_set = phrase[i][0].split('-')
  split_set_time.append(split_set)

# list of num_cur_min_p
num_cur_min_p = []
for set_num in range(len(phrase)):
  p = 0
  for line_num in range(len(lines)):
    if split_time[line_num][2] != split_set_time[set_num][2] or split_time[line_num][3] != split_set_time[set_num][3] or split_time[line_num][4] != split_set_time[set_num][4] or int(split_time[line_num][5]) < int(split_set_time[set_num][5]):
      continue
    else:
      phr = phrase[set_num][1]
      count = lines[line_num].count(phr)
      p = p + count
  num_cur_min_p.append(p)

# list of num_prior_min_p
num_prior_min_p = []
for set_num in range(len(phrase)):
  p = 0
  for line_num in range(len(lines)):
    if split_time[line_num][2] != split_set_time[set_num][2] or split_time[line_num][3] != split_set_time[set_num][3] or int(split_time[line_num][4]) + 1 != int(split_set_time[set_num][4]):
      continue
    else:
      phr = phrase[set_num][1]
      count = lines[line_num].count(phr)
      p = p + count
  num_prior_min_p.append(p)

#create the connection
conn=psycopg2.connect("dbname=milestone2 user=gb760")  #, password="123456", host="localhost", port="5432"
cur=conn.cursor()
 
# insert the data into the table PHRASE
#for i in range(len(phrase)):
#  cur.execute("INSERT INTO PHRASES(cur_time, phrase, num_cur_min_p, num_prior_min_p) VALUES(%s, %s, %s, %s)",(phrase[i][0], phrase[i][1], num_cur_min_p[i], num_prior_min_p[i]))

for i in range(len(phrase)):
  cur.execute('INSERT INTO PHRASES(cur_time, phrase, num_cur_min_p, num_prior_min_p)'+'VALUES(%s, %s, %s, %s)' , (phrase[i][0], phrase[i][1], num_cur_min_p[i], num_prior_min_p[i]))
  
# insert the data into the table TIME
#for j in range(len(cur_time)):
#  cur.execute("INSERT INTO TIME(cur_time, V_cur_min, V_prior_min, total_cur_min_num_phrase, total_prior_min_num_phrase) VALUES(%s, %s, %s, %s, %s)",(cur_time[j], V_cur_min[j], V_prior_min[j], total_cur_min_num_phrase[j], total_prior_min_num_phrase[j]))
  
for j in range(len(cur_time)):
  cur.execute('INSERT INTO TIME(cur_time, V_cur_min, V_prior_min, total_cur_min_num_phrase, total_prior_min_num_phrase)'+' VALUES(%s, %s, %s, %s, %s)' , (cur_time[j], V_cur_min[j], V_prior_min[j], total_cur_min_num_phrase[j], total_prior_min_num_phrase[j]))
  
conn.commit()  
cur.close()
conn.close()
