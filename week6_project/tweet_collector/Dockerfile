FROM python:3.6-slim

#virtual directory inside the container
WORKDIR /app

# add all files from computer to /app
ADD . /app

# install extra packages, 
RUN pip install --trusted-host pypi.python.org -r requirements.txt 

#run the scrip, but in the container
CMD python /app/get_tweets.py
