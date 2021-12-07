import argparse
import spacy
import re

open_file=open("tweet.txt")
file_tweet=open_file.read()


# clean the fata for counting
file_tweet = re.sub(r'@(\w+)','',file_tweet)
file_tweet_word = re.sub(r'[0-9]*','',file_tweet)
file_tweet_word = re.sub(r'[/]*','',file_tweet_word)
file_tweet_word = re.sub(r'[-]*','',file_tweet_word)
file_tweet_word = re.sub(r'[.]*','',file_tweet_word)
file_tweet_word = re.sub(r'[,]*','',file_tweet_word)
words = file_tweet_word.split()

parser = argparse.ArgumentParser(description='word')
parser.add_argument('--word',type=str,default='nofile',help='Enter a File Name or read from twitter API')
args=parser.parse_args()

tweet=[]
#def split_line(text):
for word in words:
  tweet.append(word)
  
def frequency(input):
  fre = 0
  for i in range(len(tweet)):
    if input == tweet[i]:
      fre = fre + 1
    else:
      fre
  return fre
  
print(frequency(args.word))
