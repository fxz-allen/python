#!/usr/bin/env python
#coding=utf-8
import sys
import json
from aliyunsdkcore import client
from aliyunsdkvpc.request.v20160428 import AllocateEipAddressRequest
from aliyunsdkvpc.request.v20160428 import UnassociateEipAddressRequest
from aliyunsdkecs.request.v20140526 import AssociateEipAddressRequest
from aliyunsdkecs.request.v20140526 import ReleaseEipAddressRequest
from aliyunsdkecs.request.v20140526 import  DescribeInstanceAttributeRequest

import time

clt = client.AcsClient('','','cn-shanghai')

def allocateEip1():
    return {"RequestId":"B51F756D-E3B4-4F00-B6A9-7CE82FD80CC4","EipAddress":"47.100.36.184","AllocationId":"eip-uf627p9i55g4isoxl8cnq"}

# 设置参数
def allocateEip():
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

    #with open('new-eip.list','w') as eip_f:
    #    eip_f.write(str(response))
    # 输出结果
    time.sleep(2)
    return response

def loadEip(eipfile):
    #response=allocateEip1()
    response=allocateEip()
    #responseR=allocateEip()
    #response=json.loads(responseR)
    if type(response) == str:
        response = eval(response)
    eip=response["EipAddress"].strip()
    eipId=response["AllocationId"].strip()
    print "create EIP ..."
    print "eip:",eip
    print "eipId:",eipId
    #with open(eipfile,"w") as eip_f:
    #    eip_f.write(str(response))
    return eipId

def getInstanceInfo(instanceId):
    request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
    request.set_accept_format('json')
    request.add_query_param('InstanceId', instanceId)
    response = clt.do_action_with_exception(request)
    print response
    print "AllocationId"
    m = eval(response)
    n = m["EipAddress"]["AllocationId"]
    l = {}
    l = {instanceId:n}
    print "local EIP :%s" % l
    return l

def bindEip(allocationId,instanceId,instancetype):
    #instancetype 绑定的对象类型。
    #取值范围：ECSInstance | HaVip
    #默认值：ECSInstance
    print "Gegin bind EIP"
    request = AssociateEipAddressRequest.AssociateEipAddressRequest()
    request.set_accept_format('json')
    request.add_query_param('AllocationId', allocationId)
    request.add_query_param('InstanceId', instanceId)
    request.add_query_param('InstanceType', instancetype)
    response = clt.do_action_with_exception(request)

def unbindEip(allocationId,instanceId):
    print "Begin to unbind EIP"
    request = UnassociateEipAddressRequest.UnassociateEipAddressRequest()
    request.set_accept_format('json')
    request.add_query_param('AllocationId', allocationId)
    request.add_query_param('InstanceId', instanceId)
    response = clt.do_action_with_exception(request)
    time.sleep(3)
    print "unbind EIP %s %s" %(allocationId,instanceId)
def releaseEip(eipId):
    print "release EIP %s " %eipId
    request = ReleaseEipAddressRequest.ReleaseEipAddressRequest()
    request.set_accept_format('json')
    request.add_query_param('AllocationId', eipId)
    response = clt.do_action_with_exception(request)


if __name__ == '__main__':
    #instanceid = sys.argv[1]
    #InstanceChargeType=
    neipfile = 'neip.list'
    oeipfile = 'oeip.list'
    ecsfile = 'ecs.list'

    with open('ecs.list','r') as f:
        for l in f:
            base = getInstanceInfo(l.strip())
            instanceId = l.strip()
            allocationId = base[l.strip()]

    # unbind EIP
            if allocationId:
                print "unbind EIP"
                unbindEip(allocationId,instanceId)

    # create EIP
            neipId = loadEip(neipfile)

    # allocate EIP
            print " bind EIP "
            print neipId,instanceId
            time.sleep(2)
            bindEip(neipId,instanceId,'ECSInstance')

    # release EIP
            if allocationId:
                print "Now to release EIP %s ..." % allocationId
                release(allocationId)

    #getInstanceId()
