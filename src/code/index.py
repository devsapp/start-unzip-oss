# -*- coding: utf-8 -*-
"""
声明：
这个函数针对文件和文件夹命名编码是如下格式：
1. mac/linux 系统， 默认是utf-8
2. windows 系统， 默认是gb2312， 也可以是utf-8

对于其他编码，我们这里尝试使用chardet这个库进行编码判断，但是这个并不能保证100% 正确，
建议用户先调试函数，如果有必要改写这个函数，并保证调试通过

Statement:
This function names and encodes files and folders as follows:
1. MAC/Linux system, default is utf-8
2. For Windows, the default is gb2312 or utf-8

For other encodings, we try to use the chardet library for coding judgment here, 
but this is not guaranteed to be 100% correct. 
If necessary to rewrite this function, and ensure that the debugging pass
"""

import oss2
import json
import os
import logging
import zipfile
import chardet

# Close the info log printed by the oss SDK
logging.getLogger("oss2.api").setLevel(logging.ERROR)
logging.getLogger("oss2.auth").setLevel(logging.ERROR)

LOGGER = logging.getLogger()


def get_zipfile_name(origin_name):  # 解决中文乱码问题
    name = origin_name
    try:
        name_bytes = origin_name.encode(encoding="cp437")
    except:
        name_bytes = origin_name.encode(encoding="utf-8")

    # the string to be detect is long enough, the detection result accuracy is higher
    detect = chardet.detect(name_bytes)
    confidence = detect["confidence"]
    detect_encoding = detect["encoding"]
    if confidence > 0.75 and (
        detect_encoding.lower() in ["gb2312", "gbk", "gb18030", "ascii", "utf-8"]
    ):
        try:
            if detect_encoding.lower() in ["gb2312", "gbk", "gb18030"]:
                detect_encoding = "gb18030"
            name = name_bytes.decode(detect_encoding)
        except:
            name = name_bytes.decode(encoding="gb18030")
    else:
        try:
            name = name_bytes.decode(encoding="gb18030")
        except:
            name = name_bytes.decode(encoding="utf-8")
    # fix windows \\ as dir segment
    name = name.replace("\\", "/")
    return name


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
    object_sizeMB = evt["oss"]["object"]["size"] / 1024 / 1024
    LOGGER.info("{} size is = {}MB".format(object_name, object_sizeMB))

    if object_sizeMB > 10240 * 0.9:
        raise RuntimeError(
            "{} size is too large; please use NAS, refer: https://github.com/zhaohang88/unzip-oss-nas".format(
                object_name
            )
        )

    file_type = os.path.splitext(object_name)[1]
    if file_type != ".zip":
        raise RuntimeError("{} filetype is not zip".format(object_name))

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

    tmpZipfile = os.path.join(tmpWorkDir, zip_name)
    bucket.get_object_to_file(object_name, tmpZipfile)

    try:
        with zipfile.ZipFile(tmpZipfile) as zip_file:
            for file_info in zip_file.infolist():
                if file_info.is_dir():
                    continue
                f_size = file_info.file_size
                if (
                    object_sizeMB + f_size / 1024 / 1024 > 10240 * 0.99
                ):  # if zip file + one file size > 0.99G, skip extract and upload
                    LOGGER.error(
                        "{} size is too large; skip extract and upload".format(f)
                    )
                    continue
                zip_file.extract(file_info.filename, tmpWorkDir)
                pathname = os.path.join(tmpWorkDir, file_info.filename)
                newkey = os.path.join(
                    newKeyPrefix, get_zipfile_name(file_info.filename)
                )
                LOGGER.info("upload to {}".format(newkey))
                bucket.put_object_from_file(newkey, pathname)
                os.remove(pathname)
    except Exception as e:
        LOGGER.error(e)
    finally:
        os.remove(tmpZipfile)
