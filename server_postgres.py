import requests
import os
import json
from datetime import datetime
import argparse
import ast
import re
import re
import io
from nltk import ngrams
import psycopg2

# To set your environment variables in your terminal run the following line:
bearer_token = os.environ.get("BEARER_TOKEN")

import sys
import spacy


nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

def clean_text(text):
    if type(text) != str:
        text = text.decode("utf-8")
    doc = re.sub(regex, '', text, flags=re.MULTILINE) # remove URLs
    sentences = []
    for sentence in doc.split("\n"):
        if len(sentence) == 0:
            continue
        sentences.append(sentence)
    doc = nlp("\n".join(sentences))
    doc = " ".join([token.lemma_.lower().strip() for token in doc
                        if (not token.is_stop)
                            and (not token.like_url)
                            and (not token.lemma_ == "-PRON-")
                            and (not len(token) < 4)])
    doc = ''.join([i for i in doc if not i.isdigit()])
    doc = remove_prefix(doc,'@') 
    doc = remove_symbol(doc,['@','.','[',']','{','}','(',')','!','#','$','%','^','*','+','/','|','-','<','>','?','_','~','`',':','"',';']) #remove all symbols in list

    return doc

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever
def remove_symbol(doc,list_s):
    for i in range(len(list_s)):
        filter(lambda x:x[0]!=list_s[i], doc.split())
        doc = " ".join(filter(lambda x:x[0]!=list_s[i],doc.split()))
    
    return doc
	
def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
        
    for response_line in response.iter_lines():
     try:
        if response_line:
            json_response = json.loads(response_line)
            json_data = json_response["data"]
         
            if json_data["lang"] == "en":
             created_at = json_data["created_at"]
             text = clean_text(json_data["text"])
             date_object = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
             date = date_object.strftime("%Y-%m-%d-%H-%M-%S")
             output = str(date) + " " + text
             fileObject = open("tweets.txt", "a")
             fileObject.write(output + "\n")
             fileObject.close()
             #print(output)
        print("Writing tweets to tweets.txt... Press ctrl+C to end...")
     except ValueError:
        print("error! Might need to export your bearer token!")



def read_file(file):
    json_data = file["data"]
    if json_data["lang"] == "en":
        created_at = json_data["created_at"]
        text = clean_text(json_data["text"])
        date_object = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
        date = date_object.strftime("%Y-%m-%d-%H-%M-%S")
        output = str(date) + " " + text
        fileObject = open("tweets.txt", "a")
        fileObject.write(output + "\n")
        fileObject.close()
     
    return print("Successfully write into tweets.txt")
   

def main():
    url = create_url()
    timeout = 0
   
    parser = argparse.ArgumentParser(description='filename')
    parser.add_argument('--filename', type=str, default='nofile',help='Enter a FIle name or read from twitter API')
    args = parser.parse_args() #print(args.filename)
   
    while args.filename == 'nofile':
     try:
        connect_to_endpoint(url)
        timeout += 1
     except KeyboardInterrupt:  
        sys.exit(0)
    else:
        with open(args.filename) as infile:
            read = infile.read()
            file = json.loads(read)
            read_file(file)

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

    cur_second = []


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
    # list of unique sets of phrase and time
    phrase = []
    len_word = []
    for line_num in range(len(lines)):
        if lines[line_num] != ' ':
            bigrams1 = ngrams(lines[line_num].split(), 1)
            bigrams2 = ngrams(lines[line_num].split(), 2)
            for gram1 in bigrams1:
                set_ = [str(words_in_line[line_num][0]), gram1[0]]
                if set_ not in phrase:
                    phrase.append(set_)
                    len_word.append(1)
            for gram2 in bigrams2:
                set_ = [str(words_in_line[line_num][0]), gram2[0] + ' ' + gram2[1]]
                if set_ not in phrase:
                    phrase.append(set_)
                    len_word.append(2)
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


    # list cur_sec in part C
    cur_sec = []
    split_time_phrase = []
    for j in range(len(phrase)):
        split = phrase[j][0].split('-')
        split_time_phrase.append(split)

    for time in split_time_phrase:
        cur_sec.append(int(time[5]))

    # count the data in part C
    num_now_min_p = []
    for set_num in range(len(phrase)):
        p = 0
        for line_num in range(len(lines)):
            if split_time[line_num][2] != split_set_time[set_num][2] or split_time[line_num][3] != split_set_time[set_num][3] or split_time[line_num][4] != split_set_time[set_num][4] or int(split_time[line_num][5]) > int(split_set_time[set_num][5]):
                continue
            else:
                phr = phrase[set_num][1]
                count = lines[line_num].count(phr)
                p = p + count
        num_now_min_p.append(p)


    # create the connection
    conn=psycopg2.connect("dbname=milestone2 user=gb760 password=123456 port=5432 ")  #, password="123456", host="localhost", port="5432"
    cur=conn.cursor()
    
    # insert the data into the table PHRASE

    cur.execute('''
    DROP TABLE phrases
    ''')

    cur.execute('''
    DROP TABLE time
    ''')

    cur.execute('''
    CREATE TABLE phrases (
    phrase VARCHAR(1000) NOT NULL,
    cur_time VARCHAR NOT NULL,
    cur_sec NUMERIC NOT NULL,
    len_word NUMERIC NOT NULL,
    num_now_min_p NUMERIC NOT NULL,
    num_cur_min_p NUMERIC NOT NULL,
    num_prior_min_p NUMERIC NOT NULL, 
    CONSTRAINT ID PRIMARY KEY(phrase, cur_time)
    )
    ''')

    cur.execute('''
    CREATE TABLE time(
    cur_time VARCHAR NOT NULL,
    V_cur_min NUMERIC NOT NULL,
    V_prior_min NUMERIC NOT NULL,
    total_cur_min_num_phrase NUMERIC NOT NULL,
    total_prior_min_num_phrase NUMERIC NOT NULL,
    PRIMARY KEY(cur_time)
    )
    ''')

    for i in range(len(phrase)):
        cur.execute('INSERT INTO PHRASES(phrase, cur_time, cur_sec, len_word, num_now_min_p, num_cur_min_p, num_prior_min_p)'+'VALUES(%s, %s,%s, %s, %s, %s, %s)' , (phrase[i][0],phrase[i][1], cur_sec[i], len_word[i], num_now_min_p[i], num_cur_min_p[i], num_prior_min_p[i]))
    
    for j in range(len(cur_time)):
        cur.execute('INSERT INTO TIME(cur_time, V_cur_min, V_prior_min, total_cur_min_num_phrase, total_prior_min_num_phrase)'+' VALUES(%s, %s, %s, %s, %s)' , (cur_time[j], V_cur_min[j], V_prior_min[j], total_cur_min_num_phrase[j], total_prior_min_num_phrase[j]))

    conn.commit() 
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
