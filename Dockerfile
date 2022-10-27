# syntax=docker/dockerfile:1

#FROM ubuntu:20.04 as stage_0
FROM python:3.10.6-buster
#FROM python:3.6.4
# Install ssh client and git
RUN apt update
RUN apt install -y openssh-client git

# Download public key for github.com
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

WORKDIR /home/
RUN cd /home

# install packages
COPY ./ ./
RUN pip install -r requirements/requirements.txt
RUN pip install -r app/requirements.txt
RUN rm -rf /root/.cache/pip


WORKDIR /home/

RUN ls
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8050"]
#CMD ["gunicorn","--workers=10", "--threads=1", "-b 0.0.0.0:8050","-t 600", "app:server"]
