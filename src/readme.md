
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、服务名、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

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

使用函数计算自动解压上传到OSS指定前缀目录的zip文件

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/start-unzip-oss/tree/main/src)

</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务：

<service>



| 服务 |  备注  |
| --- |  --- |
| 函数计算 FC |  unzip解压函数部署在函数计算 |
| 对象存储 OSS |  待解压的zip文件和解压后的文件存放在对象存储 |

</service>

推荐您拥有以下的产品权限 / 策略：
<auth>



| 服务/业务 |  权限 |  备注  |
| --- |  --- |   --- |
| 函数计算 | AliyunFCFullAccess |  创建和更新 unzip 解压函数 |
| OSS | AliyunOSSFullAccess |  创建或更新 unzip 解压函数的 OSS 触发器 |

</auth>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=start-unzip-oss) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=start-unzip-oss) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init start-unzip-oss -d start-unzip-oss `
  - 进入项目，并进行项目部署：`cd start-unzip-oss && s deploy - y`
   
</deploy>

## 应用详情

<appdetail id="flushContent">

![](http://image.editor.devsapp.cn/alibaba/4A5uks4sawFd26h9ksuc.png)

匹配解压规则的ZIP文件在上传到OSS后，会自动触发函数计算进行解压。文件解压完成后，会存储至OSS的指定目录中。


## 注意事项

- 建议使用UTF-8或GB 2312编码命名您的文件或文件夹，否则可能会出现解压后的文件或文件夹名称出现乱码、解压过程中断等问题。

- 归档或冷归档类型的文件需先解冻再解压。

- 解压单个压缩包的最大时间是2小时，超过2小时未完成的任务会解压失败。

- 建议ZIP包里面的单文件大小最好不超过1 GB，否则可能解压失败。如果出现这个场景， 请参考：[unzip-oss-with-nas](https://github.com/zhaohang88/unzip-oss-nas)

- 默认设置的函数执行时长为2h， 如果不满足需求， 自己直接调整函数的 timeout,  最大可到 24h


</appdetail>

## 使用文档

<usedetail id="flushContent">


## 参数说明


![](http://image.editor.devsapp.cn/alibaba/kD1lbEw48Er4s27212ri.png)


## 配置示例
![](http://image.editor.devsapp.cn/alibaba/lASAfezjvifa9Cwawht6.png)


## 二次开发示例
上面的示例, 解压保存回去的都还是本身触发函数的 OSS， 如果是保存到其他 OSS， 直接将 `bucket.put_object(newKey + name, file_obj)` 这样上传回 oss 的代码修改下即可， 比如：

```python
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
dst_bucket_name = "xxx-bucket"
dst_bucket = oss2.Bucket(auth, endpoint, dst_bucket_name)  
dst_bucket.put_object(newKey +  name, file_obj)

```

</usedetail>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
