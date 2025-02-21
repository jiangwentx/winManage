
# 检查当前会话是否具有管理员权限
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$adminRole = [Security.Principal.WindowsBuiltInRole]::Administrator

if (-Not $currentPrincipal.IsInRole($adminRole)) {
    # 如果不是以管理员身份运行，则重新启动脚本以获取管理员权限
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}


# 开启WinRM服务并进行快速配置
winrm quickconfig -q


# 允许未加密通信
winrm set winrm/config/client '@{AllowUnencrypted="true"}'

# 设置信任所有主机
winrm set winrm/config/client '@{TrustedHosts="*"}'

# 启用客户端的基本身份验证
winrm set winrm/config/client/auth '@{Basic="true"}'



winrm quickconfig

winrm set winrm/config/service/auth ‘@{Basic=“true”}’

winrm set winrm/config/service ‘@{AllowUnencrypted=“true”}’



# 关闭所有配置文件的Windows防火墙
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

Write-Output "Windows firemall closed。"


# 在脚本结束时暂停，以便查看输出或错误信息
Read-Host "enter any key exit..."