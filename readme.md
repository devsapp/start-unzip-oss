# start-unzip-oss 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-unzip-oss&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-unzip-oss" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-unzip-oss&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-unzip-oss" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-unzip-oss&type=packageDownload">
  </a>
</p>

<description>

> ***快速部署自动解压上传到OSS指定前缀目录的zip文件的应用到阿里云函数计算***

</description>

<table>
</table>

<codepre id="codepre">

</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=start-unzip-oss) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=start-unzip-oss)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init start-unzip-oss -d start-unzip-oss`   
    - 进入项目，并进行项目部署：`cd start-unzip-oss && s deploy -y`

</deploy>

<appdetail id="flushContent">

# 应用详情

![](https://img.alicdn.com/imgextra/i1/O1CN01V092Oa1p04ieFtASz_!!6000000005297-2-tps-1220-320.png)

通过给函数创建 OSS 触发器， 用户只需要给对应的 OSS 指定前缀目录上传 zip 文件， 就会自动触发解压函数执行， 解压函数会把解压后的文件和文件夹转存回 OSS

通过 Serverless Devs 开发者工具，您只需要几步，就可以体验 Serverless 架构，带来的降本提效的技术红利。

## 声明

这个应用函数针解压对文件和文件夹命名编码是如下格式：
1. mac/linux 系统， 默认是utf-8
2. windows 系统， 默认是gb2312(或者gb18030)， 也可以是utf-8

对于其他编码，我们这里尝试使用chardet这个库进行编码判断， 但是这个并不能保证100% 正确，
建议用户先调试函数，如果有必要改写这个函数，并保证调试通过
## Tips:
上面的示例, 解压保存回去的都还是本身触发函数的 OSS， 如果是保存到其他 OSS， 直接将 `bucket.put_object(newKey + name, file_obj)` 这样上传回 oss 的代码修改下即可， 比如：

```python
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
dst_bucket_name = "xxx-bucket"
dst_bucket = oss2.Bucket(auth, endpoint, dst_bucket_name)  
dst_bucket.put_object(newKey +  name, file_obj)
```

</appdetail>

<devgroup>

## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
|--- | --- | --- |
| <center>微信公众号：\`serverless\`</center> | <center>微信小助手：\`xiaojiangwh\`</center> | <center>钉钉交流群：\`33947367\`</center> | 

</p>

</devgroup>