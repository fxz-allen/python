# coding:utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import os
import urllib2
import json

MAIL_URL = "http://10.144.148.115:8599/send/email"


def call_service(service_url, data):
    req = urllib2.Request(service_url)
    req.add_header('Content-Type', 'application/json')

    strdata = json.dumps(data)
    try:
        response = urllib2.urlopen(req, strdata)
    except Exception, e:
        return None

    code = response.getcode()
    if code != 200:
        return None

    resp = response.read()
    try:
        r = json.loads(resp)
    except Exception:
        return None

    ret = r.get('ret', None)
    if(None == ret):
        ret = r.get('errcode', None)

    if ret != 1:
        return None

    return r


def check_file():
    t = time.localtime(time.time()-86400)
    prefix = "/home/fengxinzhi/nginx-%d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday)
    cnt = 0

    files = []

    ## 获取修改时间在21点-24点之间的文件
    while(1):
        path = prefix + "_%05d" % cnt
        print path
        try:
            cnt += 1
            statinfo=os.stat(path)
            hour = time.localtime(statinfo.st_mtime).tm_hour

            if hour >=21 and hour <=24:
                files.append(path)
        except Exception,e:
            print e
            break
    return files


def parse_log(path, action_map):
    f = open(path)
    qps_map = {}
    qps = {}
    for l in f:
        sections = l.strip().split("HTTP")

        tstr = sections[0].split(",")[0].split('.')[0]

        # parse uri
        uri = sections[0].strip().split()[-1]
        uri = uri.split("?")[0].strip()

        fields = uri.replace("//", "/").split("/")
        if len(fields) < 3:
            continue

        uri = "/" + fields[1] + "/" + fields[2]

        # parse response time
        seconds = sections[1].strip().split()

        if uri not in action_map:
            action_map[uri] = 1
        else:
            action_map[uri] += 1

        qps_map.setdefault(uri, {})
        qps_map[uri][tstr] = qps_map[uri].get(tstr, 0) + 1

    f.close()

    for uri, v in qps_map.items():
        m = 0
        for tstr, cnt in v.items():
            if cnt > m:
                m = cnt
        qps[uri] = m
    return action_map, qps

def send(action, qps):
    htable = []

    # 21点-到24点调用次数统计
    data = {}
    data["cap"] = u"21-24点调用次数统计"
    data["head"] = [u"uri", u"总次数"]

    stats = []
    for k, v in action:
        stats.append([k, str(v)])

    data["table"] = stats
    htable.append(data)


    # 21点-到24点最大qps统计
    data = {}
    data["cap"] = u"21-24点qps统计"
    data["head"] = [u"uri", u"qps"]

    stats = []
    for k, v in qps:
        stats.append([k, str(v)])
    data["table"] = stats
    htable.append(data)


    t = time.localtime(time.time()-86400)
    day = "%d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday)

    mail = {}
    #mail['to'] = ["server@xiaochuankeji.cn", "guolin2014@xiaochuankeji.cn", "yangchenghu2014@xiaochuankeji.cn", "zhaomingliang2014@xiaochuankeji.cn"]
    mail['to'] = ["fengxinzhi2014@xiaochuankeji.cn"]
    mail['sender'] = "最右统计"
    mail['subject'] = day + " 服务器接口调用统计"
    mail['htable'] = htable

    call_service(MAIL_URL, mail)


if __name__ == "__main__":
    files = check_file()

    action_map = {}
    qps_map = {}
    for path in files:
        print int(time.time()), path
        action_map, qps = parse_log(path, action_map)
        for uri, cnt in qps.items():
            maxcnt = qps_map.get(uri, 0)
            if cnt > maxcnt:
                qps_map[uri] = cnt

    actions = sorted(action_map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    qpslist = sorted(qps_map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

    send(actions, qpslist)
