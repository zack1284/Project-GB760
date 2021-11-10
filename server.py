import requests
import os
import json
from datetime import datetime
import argparse
import ast

# To set your environment variables in your terminal run the following line:
#export BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAKVkVAEAAAAAUnzDwyYuL6V%2BUB4%2FOc%2BsJBHo%2BL0%3DPy1K9NUa4V3W8KU9vruHBcMwYN8k7gE855Hkpt4J2mDe3i5Ak5'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang&expansions=author_id&user.fields=created_at"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            json_data = json_response["data"]
            if json_data["lang"] == "en":
             created_at = json_data["created_at"]
             text = json_data["text"]
             date_object = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ')
             date = date_object.strftime("%Y-%m-%d-%H-%M-%S")
             output = str(date) + " " + text
             fileObject = open("temp.txt", "a")
             fileObject.write(output + "\n")
             fileObject.close()
             print(output)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def read_files(data):
     print(data)



def main():
   url = create_url()
   timeout = 0
   
   parser = argparse.ArgumentParser(description='filename')
   parser.add_argument('--filename', type=str, default='nofile',help='Enter a FIle name or read from twitter API')
   args = parser.parse_args() #print(args.filename)
   
   while args.filename == 'nofile':
      connect_to_endpoint(url)
      timeout += 1
   else:
    with open(args.filename) as f:
     read_files(f.read())


if __name__ == "__main__":
    main()
    
    
    
