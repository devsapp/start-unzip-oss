# -*- coding: utf-8 -*-
# zip 文件里面包含超多小文件的时候， 可以采用这个方案优化解压上传速度

import oss2
import json
import os
import logging
import zipfile
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Close the info log printed by the oss SDK
logging.getLogger("oss2.api").setLevel(logging.ERROR)
logging.getLogger("oss2.auth").setLevel(logging.ERROR)

LOGGER = logging.getLogger()


def handler(event, context):
    """
    The object from OSS will be decompressed automatically .
    param: event:   The OSS event json string. Including oss object uri and other information.
        For detail info, please refer https://help.aliyun.com/document_detail/70140.html?spm=a2c4g.11186623.6.578.5eb8cc74AJCA9p#OSS

    param: context: The function context, including credential and runtime info.

        For detail info, please refer to https://help.aliyun.com/document_detail/56316.html#using-context
    """
    evt_lst = json.loads(event)
    creds = context.credentials
    auth = oss2.StsAuth(
        creds.access_key_id, creds.access_key_secret, creds.security_token
    )

    evt = evt_lst["events"][0]
    bucket_name = evt["oss"]["bucket"]["name"]
    endpoint = "oss-" + evt["region"] + "-internal.aliyuncs.com"
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    object_name = evt["oss"]["object"]["key"]

    if "ObjectCreated:PutSymlink" == evt["eventName"]:
        object_name = bucket.get_symlink(object_name).target_key
        if object_name == "":
            raise RuntimeError(
                "{} is invalid symlink file".format(evt["oss"]["object"]["key"])
            )

    file_type = os.path.splitext(object_name)[1]

    if file_type != ".zip":
        raise RuntimeError("{} filetype is not zip".format(object_name))

    LOGGER.info("start to decompress zip file = {}".format(object_name))

    lst = object_name.split("/")
    zip_name = lst[-1]
    PROCESSED_DIR = os.environ.get("PROCESSED_DIR", "")
    RETAIN_FILE_NAME = os.environ.get("RETAIN_FILE_NAME", "")
    if RETAIN_FILE_NAME == "false":
        newKeyPrefix = PROCESSED_DIR
    else:
        newKeyPrefix = os.path.join(PROCESSED_DIR, zip_name)
    newKeyPrefix = newKeyPrefix.replace(".zip", "/")

    tmpWorkDir = "/tmp/{}".format(context.request_id)
    if not os.path.exists(tmpWorkDir):
        os.makedirs(tmpWorkDir)

    tmpZipfile = "{}/{}".format(tmpWorkDir, zip_name)
    bucket.get_object_to_file(object_name, tmpZipfile)

    with zipfile.ZipFile(tmpZipfile) as zip_file:
        zip_list = zip_file.namelist()
        for f in zip_list:
            zip_file.extract(f, tmpWorkDir)

    os.remove(tmpZipfile)
    try:
        listDir(tmpWorkDir, bucket, newKeyPrefix)
    except Exception as e:
        LOGGER.error(e)
    finally:
        subprocess.check_call("rm -rf {}".format(tmpWorkDir), shell=True)


def upload_file(bucket, newkey, pathname):
    """用于上传单个文件的辅助函数"""
    bucket.put_object_from_file(newkey, pathname)


def listDir(destDir, bucket, newKeyPrefix):
    # 创建一个最大线程数为3的线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        for filename in os.listdir(destDir):
            pathname = os.path.join(destDir, filename)
            if os.path.isdir(pathname):
                listDir(pathname, bucket, newKeyPrefix)
            else:
                newkey = os.path.join(newKeyPrefix, "/".join(pathname.split("/")[3:]))
                # 提交任务到线程池
                executor.submit(upload_file, bucket, newkey, pathname)
