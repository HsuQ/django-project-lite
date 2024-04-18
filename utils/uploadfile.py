import oss2
import uuid
from django.conf import settings

ossAuth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)


def uploadFile(file):
    bucket = settings.BUCKET
    ossBucket = oss2.Bucket(ossAuth, settings.ENDPOINT, bucket)
    # result = ossBucket.put_object_from_file(remoteName, filepath)

    # 生成文件编号，如果文件名重复的话在oss中会覆盖之前的文件
    number = uuid.uuid4()
    # 生成文件名

    base_fil_name = str(number) + '.jpg'
    # 生成外网访问的文件路径
    file_name = settings.FILE_PREFIX + base_fil_name
    headers = {
        "Content-Type": "image/jpg",
        "Cache-Control": "public, no-cache",
        "Content-Disposition": 'attachment',
        "x-oss-force-download": 'true'
    }
    res = ossBucket.put_object(base_fil_name, file, headers)
    # print(res.status)
    return res.status, file_name


def uploadFileExcel(file):
    bucket = settings.BUCKET
    ossBucket = oss2.Bucket(ossAuth, settings.ENDPOINT, bucket)
    # result = ossBucket.put_object_from_file(remoteName, filepath)

    # 生成文件编号，如果文件名重复的话在oss中会覆盖之前的文件
    number = uuid.uuid4()
    # 生成文件名

    base_fil_name = str(number) + '.xlsx'
    # 生成外网访问的文件路径
    file_name = settings.FILE_PREFIX + base_fil_name
    headers = {
        # "Content-Type": "image/jpg",
        "Cache-Control": "public, no-cache",
        "Content-Disposition": 'attachment',
        "x-oss-force-download": 'true'
    }
    # res = ossBucket.put_object(base_fil_name, file, headers)
    res = ossBucket.put_object_from_file(base_fil_name, file, headers)
    # print(res.status)
    return res