from flask import Flask, request
import json
# from datetime import datetime
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
# from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest

rc_format = 'json'
app = Flask(__name__)

@app.route("/alidns", methods=["GET", "POST"])
def alidns():
    if request.method == 'GET':  # 获取访问方式 GET
        data = {
            'domain': request.args["domain"],
            'access_key_id': request.args["id"],
            'access_key_secret': request.args["secret"],
            'r_record': request.args["record"],
            'ip': request.args["ip"]
        }
        try:
            records = check_records(data)
            if 'Code' not in records:
                for record in records['DomainRecords']['Record']:
                    if record["Type"] == 'A' and record['RR'] == data['r_record']:
                        if record['Value'] != data['ip']:
                            update_dns(data, record, rc_format)
                            return "0"
                        else:
                            return "1"
            else:
                return "2"
        except:
            pass

def check_records(data):
    clt = client.AcsClient(data['access_key_id'], data['access_key_secret'], 'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(data['domain'])
    request.set_accept_format(rc_format)
    result = clt.do_action(request).decode('utf-8')
    result = json.JSONDecoder().decode(result)
    return result

# 更新阿里云域名解析记录信息
def update_dns(data, record,dns_format):
    rc_type = record['Type']  # 记录类型, DDNS填写A记录
    rc_value = data['ip']  # 新的解析记录值
    rc_record_id = record['RecordId']  # 记录ID
    rc_ttl = record['TTL']  # 解析记录有效生存时间TTL,单位:秒
    clt = client.AcsClient(data['access_key_id'], data['access_key_secret'], 'cn-hangzhou')
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(data['r_record'])
    request.set_Type(rc_type)
    request.set_Value(rc_value)
    request.set_RecordId(rc_record_id)
    request.set_TTL(rc_ttl)
    request.set_accept_format(dns_format)
    result = clt.do_action(request)
    return result

if __name__ == '__main__':
    # 设置host，端口8080，threaded=True 代表开启多线程
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
