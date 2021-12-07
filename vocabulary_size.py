import spacy
import re


#define how to create a list of unique words
def unique_list(filename):
    open_file=open(filename)
    file_tweet =open_file.read()
    file_tweet = re.sub(r'@(\w+)','',file_tweet)
    file_tweet_word = re.sub(r'[0-9]*','',file_tweet)
    file_tweet_word = re.sub(r'[/]*','',file_tweet_word)
    file_tweet_word = re.sub(r'[-]*','',file_tweet_word)
    file_tweet_word = re.sub(r'[.]*','',file_tweet_word)
    file_tweet_word = re.sub(r'[,]*','',file_tweet_word)
    words = file_tweet_word.split()
    unique = []
    for word in words:
        if word not in unique:
            unique.append(word)
    return unique

def count_unique():
    unique_word = unique_list("tweet.txt")
    count = len(unique_word)
    print(f"The file tweet.txt have {count} unique words.")

if __name__ == "__main__":
    count_unique()