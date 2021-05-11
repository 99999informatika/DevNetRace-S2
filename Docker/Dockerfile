# syntax=docker/dockerfile:1
FROM ubuntu
WORKDIR /app
COPY * /app/
RUN ls -l
RUN apt-get update && apt-get -y install python3 python3-pip
RUN pip3 install -r requirements.txt
RUN ["chmod", "+x", "/app/start.py"]
CMD ["/app/start.py"]
