# coding:utf-8
import oss2
import os
import sys
import getopt
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo

auth = oss2.Auth('','')
bucket = oss2.Bucket(auth,'','rec101')
basepath = '/home/fengxinzhi/'
#basepath = '/data/tieba/log/tbstat/'
bucketname = 'rec101'

def ossdir(dirname):
    localpath = u"%s%s"%(basepath,dirname)
    for i in os.listdir(localpath):
        localfile = os.path.join(basepath,dirname,i)
        print localfile
        destfile = u"%s/%s"%(dirname,i)
        print "destfile:%s" %destfile
        log2oss(dirname,destfile,localfile)

def log2oss(dirname,destfile,localfile):
    destfile = os.path.basename(localfile)
    destfile = os.path.join(dirname,os.path.basename(localfile))
    print destfile
    print "upload ...."
    total_size = os.path.getsize(localfile)
    part_size = determine_part_size(total_size,preferred_size = 100 * 1000 * 1024)

    upload_id = bucket.init_multipart_upload(destfile).upload_id
    parts = []

    with open(localfile, 'rb') as fileobj:
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(destfile, upload_id, part_number,
                                        SizedFileAdapter(fileobj, num_to_upload))
            parts.append(PartInfo(part_number, result.etag))
            offset += num_to_upload
            part_number += 1
    # 完成分片上传
    bucket.complete_multipart_upload(destfile, upload_id, parts)
    # 验证一下
    with open(localfile, 'rb') as fileobj:
        assert bucket.get_object(destfile).read() == fileobj.read()
    '''
    #oss2.resumable_upload(bucket,destfile,localfile)
    oss2.resumable_upload(bucket,destfile,localfile,
            store = oss2.ResumableStore(root='/tmp'),
            multipart_threshold=100*1024,
            part_size = 1000*1024,
            num_threads = 4
            )
    '''

if __name__ == '__main__':
    ossdir(sys.argv[1])
