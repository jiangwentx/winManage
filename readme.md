# python管理多台win10

使用场景:有多台win10需要后台远程管理。

利用windows提供得winrm服务，可以实现远程执行powershell脚本

server-manage-all-mysql.py包含查询所有会话，超过指定时间终止会话，重置密码，更新状态函数。mysql记录所有状态。

# 安装依赖
```bash 
pip install mysql-connector-python
```



# 快速开始

- 执行win10openwinrm.ps1,利用winrm的5985端口，远程执行powershell命令。
- docker启动mysql8.0,执行V1.0.1__init.sql。
- 执行python server-manage-all-mysql.py。



# 补充：

在很多企业会使用闲置的 Windows 机器作为临时服务器，有时候我们想远程调用里面的程序或查看日志文件

Windows 内置的服务「 winrm」可以满足我们的需求

它是一种基于标准简单对象访问协议（ SOAP ）的防火墙友好协议，允许来自不同供应商的硬件和操作系统进行互操作

官网：https://docs.microsoft.com/en-us/windows/win32/winrm/portal

以 Windows 10 系统机器为例

具体操作步骤如下：

```bash 
winrm quickconfig -q

允许未加密通信

winrm set winrm/config/client '@{AllowUnencrypted="true"}'

设置信任所有主机

winrm set winrm/config/client '@{TrustedHosts="*"}'

启用客户端的基本身份验证

winrm set winrm/config/client/auth '@{Basic="true"}'

winrm quickconfig

winrm set winrm/config/service/auth ‘@{Basic=“true”}’

winrm set winrm/config/service ‘@{AllowUnencrypted=“true”}’


```

执行完如上操作，就可以使用python愉快的操作win10啦~~~
