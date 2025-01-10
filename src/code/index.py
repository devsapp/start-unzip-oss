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
import shutil

# Close the info log printed by the oss SDK
logging.getLogger("oss2.api").setLevel(logging.ERROR)
logging.getLogger("oss2.auth").setLevel(logging.ERROR)

LOGGER = logging.getLogger()


def get_zipfile_name(origin_name):  # 解决中文乱码问题
    name = origin_name
    try:
        # 尝试常见编码
        name_bytes = origin_name.encode("cp437")
        # macOS 系统可能使用 utf-8-mac 编码
        try:
            name = name_bytes.decode("utf-8-mac")
        except:
            # 尝试其他常见编码
            for encoding in ["utf-8", "gb18030", "cp437"]:
                try:
                    name = name_bytes.decode(encoding)
                    break
                except:
                    continue
    except:
        # 如果无法编码为 cp437，直接尝试 utf-8 和 gb18030
        for encoding in ["utf-8", "gb18030"]:
            try:
                name = origin_name.encode(encoding).decode(encoding)
                break
            except:
                continue

    # 替换路径分隔符
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

    WORK_DIR = os.environ.get("WORK_DIR", "/tmp")

    if WORK_DIR == "/tmp" and object_sizeMB > 10240 * 0.9:
        raise RuntimeError(
            "{} size is too large; Please use NAS and set the WORK_DIR environment variable to specify the NAS mount directory. For reference, see: https://help.aliyun.com/zh/functioncompute/fc-3-0/user-guide/configure-a-nas-file-system-1".format(
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

    tmpWorkDir = "{}/{}".format(WORK_DIR, context.request_id)
    if not os.path.exists(tmpWorkDir):
        os.makedirs(tmpWorkDir)

    tmpZipfile = os.path.join(tmpWorkDir, zip_name)
    bucket.get_object_to_file(object_name, tmpZipfile)

    try:
        with zipfile.ZipFile(tmpZipfile) as zip_file:
            for file_info in zip_file.infolist():
                # 跳过 macOS 系统生成的文件
                if "__MACOSX" in file_info.filename or file_info.filename.endswith(".DS_Store"):
                    continue

                # 跳过文件夹
                if file_info.is_dir():
                    continue

                # 处理文件
                f_size = file_info.file_size
                if (
                    WORK_DIR == "/tmp"
                    and object_sizeMB + f_size / 1024 / 1024 > 10240 * 0.99
                ):
                    LOGGER.error(
                        "{} size is too large; skip extract and upload. Please use NAS and set the WORK_DIR environment variable to specify the NAS mount directory. For reference, see: https://help.aliyun.com/zh/functioncompute/fc-3-0/user-guide/configure-a-nas-file-system-1".format(
                            file_info.filename
                        )
                    )
                    continue

                # 解压文件
                zip_file.extract(file_info.filename, tmpWorkDir)
                pathname = os.path.join(tmpWorkDir, file_info.filename)

                # 获取处理后的文件名
                cleaned_filename = get_zipfile_name(file_info.filename)

                # 构建新的 OSS 路径
                newkey = os.path.join(newKeyPrefix, cleaned_filename)
                LOGGER.info("upload to {}".format(newkey))

                # 上传文件
                bucket.put_object_from_file(newkey, pathname)
                os.remove(pathname)
    except Exception as e:
        LOGGER.error(e)
    finally:
        os.remove(tmpZipfile)
        shutil.rmtree(tmpWorkDir)