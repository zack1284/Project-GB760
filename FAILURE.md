1.Problem: Exception: Request returned an error: 401 {"title":"Unauthorized","detail":"Unauthorized","type":"about:blank","status":401}
At the begining, I haven't got my own bearer token, so I borrowed the bearer token from my friend. I thoguth this errir is raised because of using other person's token. Then I found out later, I need to export bearer token outside the server.py.

2.Problem: When transforming ISO 8601 date format to  the date format we want, I faild many times.
Our date format looks like this "2010-05-08T23:41:54.000Z", I was stuck with the last three zeros infront of Z. Eventually, I found out that means microsecond, so I used %f to solve it at the end.
The code:
     date_object = datetime.strptime(created_at,'%Y-%m-%dT%H:%M:%S.%fZ') #read the ISO8601 to datetime
     date = date_object.strftime("%Y-%m-%d-%H-%M-%S") #transform to our format

3.Problem: When ever we try to stop the code with ctrl+c, there will be a lot of error messsage due to keyboardinterrupt, and it doesn't look nice.
I put a try except python code to catch keyboardInterruption, So it won't generate a lot of error messages.
The code:
    try:
      connect_to_endpoint(url)
      timeout += 1
    except KeyboardInterrupt:  
      sys.exit(0)
