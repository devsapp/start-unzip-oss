
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# start-unzip-oss-dipper 帮助文档

<description>

本案例是将解压zip文件工具 unzip，快速创建并部署到阿里云函数计算 FC。

</description>

<codeUrl>



</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>



| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |
| 对象存储 |  AliyunOSSFullAccess | [帮助文档](https://help.aliyun.com/zh/oss) [计费文档](https://help.aliyun.com/zh/oss/product-overview/billing) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
:fire: 通过 [Dipper 应用中心](https://devs.console.aliyun.com/applications/createtemplate=start-unzip-oss-dipper) ，[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://devs.console.aliyun.com/applications/createtemplate=start-unzip-oss-dipper) 该应用。
   
</appcenter>
<deploy>

</deploy>

## 案例介绍

<appdetail id="flushContent">

本案例是将zip文件进行 unzip 解压，快速创建并部署到阿里云函数计算 FC。

匹配解压规则的ZIP文件在上传到OSS后，会自动触发函数计算进行解压。文件解压完成后，会存储至OSS的指定目录中。

- 建议使用 UTF-8 或 GB 2312 编码命名您的文件或文件夹，否则可能会出现解压后的文件或文件夹名称出现乱码、解压过程中断等问题。

- 归档或冷归档类型的文件需先解冻再解压。

- 解压单个压缩包的最大时间是 2 小时，超过 2 小时未完成的任务会解压失败。

- 建议 ZIP 包里面的单文件大小最好不超过 1 GB，否则可能解压失败。如果出现这个场景， 请参考：[unzip-oss-with-nas](https://github.com/zhaohang88/unzip-oss-nas)

- 默认设置的函数执行时长为2h， 如果不满足需求， 自己直接调整函数的 timeout,  最大可到 24h

![](http://image.editor.devsapp.cn/alibaba/4A5uks4sawFd26h9ksuc.png)

</appdetail>

## 使用流程

<usedetail id="flushContent">

### 查看部署的案例

- 部署时， 选择的OSS存储桶名、触发的前缀目录名以及解压后的目录

- 部署完成后，在oss对象存储中找到相应的OSS存储桶名，向该存储桶指定前缀目录上传zip文件，等一会， 可以在解压后的目录查看到解压后的文件及文件夹

#### 参数说明

![](http://image.editor.devsapp.cn/alibaba/kD1lbEw48Er4s27212ri.png)


#### 配置示例
![](http://image.editor.devsapp.cn/alibaba/lASAfezjvifa9Cwawht6.png)


### 二次开发
您可以通过云端控制台的开发功能进行二次开发, 上面的示例, 解压保存回去的都还是本身触发函数的 OSS， 如果是保存到其他 OSS， 直接将 `bucket.put_object(newKey + name, file_obj)` 这样上传回 oss 的代码修改下即可， 比如：

```python
auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
dst_bucket_name = "xxx-bucket"
dst_bucket = oss2.Bucket(auth, endpoint, dst_bucket_name)
dst_bucket.put_object(newKey +  name, file_obj)

```

</usedetail>

## 注意事项

<matters id="flushContent">
</matters>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://images.devsapp.cn/fc-faq/33947367.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
