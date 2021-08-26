#
FROM python:alpine3.7
RUN apk update && apk add --no-cache gcc g++ python3-dev unixodbc-dev


RUN python3 -m pip install --upgrade pip3 && pip3 install aliyun-python-sdk-alidns && pip3 install flask&& apk del tzdata \
&& rm -rf /var/cache/apk/* \
&& rm -rf /root/.cache \
&& rm -rf /tmp/*
COPY app/ /app/
WORKDIR /app
EXPOSE 80
CMD ["python3","flask_aliyun_ddns.py"]
