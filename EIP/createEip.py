#!/usr/bin/env python
#coding=utf-8
import sys
import json
from aliyunsdkcore import client
from aliyunsdkvpc.request.v20160428 import AllocateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import UnassociateEipAddressRequest

clt = client.AcsClient('','','')

# 设置参数
def post():
    request = AllocateEipAddressRequest.AllocateEipAddressRequest()
    request.set_accept_format('json')

    #request.add_query_param('InstanceId', instanceid)
    #付款形式
    request.add_query_param('InstanceChargeType', 'PostPaid')
    #带宽类型
    request.add_query_param('InternetChargeType', 'PayByTraffic')
    #带宽数
    request.add_query_param('Bandwidth', '40')

    # 发起请求
    #response = clt.do_action(request)
    response = clt.do_action_with_exception(request)

    with open('eip.txt',w) as eip_f:
        eip_f.write(response)
    # 输出结果
    return response

def get():
    responseR=post()
    response=json.loads(responseR)
    eip=response["EipAddress"]
    eipId=response["AllocationId"]
    print "eip:",eip
    print "eipId:",eipId
    with open('eip.txt',w) as eip_f:
        eip_f.write(response)

def getInstanceId():



def bindEip():
    request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
    request.set_accept_format('json')


def unbindEip():
        request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
        request.set_accept_format('json')


if __name__ == '__main__':
    #instanceid = sys.argv[1]
    #InstanceChargeType=
    get()
