# python用winrm远程操作win10

使用场景:有多台win10需要后台远程管理

server-manage-all-mysql.py包含查询所有会话，超过指定时间终止会话，重置密码，更新状态函数。

# 安装依赖
```bash 
pip install mysql-connector-python
```



# 快速开始

- 执行win10openwinrm.ps1,利用winrm的5985端口，远程执行powershell命令。
- docker启动mysql8.0,执行V1.0.1__init.sql。
- 执行python server-manage-all-mysql.py。

