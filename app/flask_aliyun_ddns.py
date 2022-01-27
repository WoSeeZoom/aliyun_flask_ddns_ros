from flask import Flask, request
import os, json
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest, UpdateDomainRecordRequest


rc_format = 'json'
app = Flask(__name__)

access_key_id = os.environ['ACCESS_KEY_ID']
access_key_secret = os.environ['ACCESS_KEY_SECRET']
domain = "yunys.top"
subdomains = ['home', 'jp']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':  # 获取访问方式 GET
        ip = request.args["ip"]
        records = check_records()
        update_list = []
        for record in records['DomainRecords']['Record']:
            if record["Type"] == 'A' and record['RR'] in subdomains:
                if record['Value'] != ip:
                    update_dns(ip, record, rc_format)
                    update_list.append(record['RR'])
        if update_list:
            msg = "subdomain:{}更新完成".format(','.join(update_list))
        else:
            msg = "finish"
        return msg


def check_records():
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(domain)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request).decode('utf-8')
    result = json.JSONDecoder().decode(result)
    return result

# 更新阿里云域名解析记录信息
def update_dns(ip, record, dns_format):
    rc_type = record['Type']  # 记录类型, DDNS填写A记录
    rc_value = ip  # 新的解析记录值
    rc_record_id = record['RecordId']  # 记录ID
    rc_ttl = record['TTL']  # 解析记录有效生存时间TTL,单位:秒
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(record['RR'])
    request.set_Type(rc_type)
    request.set_Value(rc_value)
    request.set_RecordId(rc_record_id)
    request.set_TTL(rc_ttl)
    request.set_accept_format(dns_format)
    result = clt.do_action_with_exception(request)
    return result


if __name__ == '__main__':
    # 设置host，端口8080，threaded=True 代表开启多线程
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
