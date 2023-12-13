FROM python:3.6
MAINTAINER Madison Bahmer <madison.bahmer@istresearch.com>

# os setup
RUN apt-get update && apt-get -y install \
  # python-lxml \
  build-essential \
  libssl-dev \
  libffi-dev \
  python-dev \
  libxml2-dev \
  libxslt1-dev \
  && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/gourd/crawler
WORKDIR /usr/gourd/crawler

# install requirements
COPY utils /usr/gourd/utils
COPY crawler/requirements.txt /usr/gourd/crawler/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /usr/gourd/utils

# move codebase over
COPY crawler /usr/gourd/crawler

# override settings via localsettings.py
COPY settings.py /usr/gourd/crawler/crawling/localsettings.py

# set up environment variables

