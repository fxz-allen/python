# coding:utf-8
# 实现断点续传，传输小于5GB文件
import oss2
import os
import sys
import getopt

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
    with open(localfile,'rb') as ossfile:
        destfile = os.path.basename(localfile)
        destfile = os.path.join(dirname,os.path.basename(localfile))
        print destfile
        print "upload ...."
        #oss2.resumable_upload(bucket,destfile,localfile)
        oss2.resumable_upload(bucket,destfile,localfile,
                store = oss2.ResumableStore(root='/tmp'),
                multipart_threshold=100*1024,
                part_size = 1000*1024,
                num_threads = 4
                )

if __name__ == '__main__':
    sys.argv[1]
    ossdir(sys.argv[1])
