FROM tiangolo/meinheld-gunicorn-flask:python3.8

RUN apt-get install curl
RUN apt-get install apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

RUN apt-get update
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN apt-get install mssql-tools unixodbc-dev -y

RUN apt-get update \
    && apt-get install gcc \
    && apt-get install --reinstall build-essential -y
    
COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

EXPOSE 80

COPY ./app /app