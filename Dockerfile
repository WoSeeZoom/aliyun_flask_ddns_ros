FROM python:3.7-alpine
#RUN apk update && apk add --no-cache gcc g++ python3-dev unixodbc-dev
RUN apk update && apk upgrade

RUN pip install --upgrade pip
RUN pip install aliyun-python-sdk-alidns -i http://mirrors.aliyun.com/pypi/simple/
RUN pip install flask -i http://mirrors.aliyun.com/pypi/simple/
RUN apk del tzdata && rm -rf /var/cache/apk/* && rm -rf /root/.cache && rm -rf /tmp/*
#RUN python -m pip install --upgrade pip && pip install aliyun-python-sdk-alidns && pip install flask && apk del tzdata && rm -rf /var/cache/apk/* && rm -rf /root/.cache && rm -rf /tmp/*
COPY app/ /app/
WORKDIR /app
EXPOSE 80
CMD ["python","flask_aliyun_ddns.py"]


