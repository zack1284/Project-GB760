import argparse

def main():
   open_file=open("tweet.txt")
   file_tweet =open_file.read()
   
   parser = argparse.ArgumentParser(description='word')
   parser.add_argument('--word', type=str, default='nofile',help='Enter a FIle name or read from twitter API')
   args = parser.parse_args() #print(args.filename)
   
   print(args.word)

if __name__ == "__main__":
    main()
