#
#     Copyright (c) 2022 World Wide Technology
#     All rights reserved.
#
#     author: @joelwking
#     written:  21 Jan 2022
#     references:
#       activate virtualenv: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
#       https://github.com/wwt/network-endpoint-mapper
#
FROM python:3.8.10-slim-buster
ENV VIRTUAL_ENV=/opt/soar
LABEL maintainer="Joel W. King" email="programmable.networks@gmail.com"
RUN apt update && \
    apt -y install git && \
    apt -y install python3-venv && \
    pip3 install --upgrade pip 
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip3 install -r requirements.txt

ADD https://raw.githubusercontent.com/joelwking/Phantom-Cyber/master/REST_ingest/PhantomIngest.py /code/PhantomIngest.py
ENV PYTHONPATH=/code
#
#   The virtual environment is /opt/soar