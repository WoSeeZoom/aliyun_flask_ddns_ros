#
FROM python:3.9-alpine3.14
RUN apk update && apk add --no-cache gcc g++ python3-dev unixodbc-dev
RUN python --version
#RUN python -m pip install --upgrade pip && pip install aliyun-python-sdk-alidns && pip install flask && apk del tzdata && rm -rf /var/cache/apk/* && rm -rf /root/.cache && rm -rf /tmp/*
COPY app/ /app/
WORKDIR /app
EXPOSE 80
CMD ["python","flask_aliyun_ddns.py"]
