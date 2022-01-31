FROM python:3.8

#virtual directory inside the container
WORKDIR /app

# add all files from computer to /app
ADD . /app

# install extra packages, 
RUN pip install --trusted-host pypi.python.org -r requirements.txt 

#run the scrip, but in the container/python /app/etl.py
CMD python /app/slackbot.py 
