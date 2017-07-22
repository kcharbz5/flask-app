FROM python:3.5

#RUN apt-get update -yqq \
#    && apt-get install -yqq \ 
#    python3-pip \ 
#    python3-dev \ 
#    build-essential \
#    mysql-client

RUN mkdir /app
COPY app /app
WORKDIR /app

COPY reqs.txt reqs.txt
RUN pip3 install -r reqs.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]

