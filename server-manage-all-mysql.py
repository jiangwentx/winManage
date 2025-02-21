import winrm
import re
import random
import hashlib
import string
import time
from datetime import datetime, timedelta
import mysqlutil as m

#超管用户report和对外用户test需要自己创建并添加为管理用户组

# 所有管理的虚拟机用户名和密码设置为sqwa/suqian@456
orgin_username = "test"
orgin_passwd = "123456"

# 超管账户
admin_name = "report"
admin_passwd = "123456"

# 定义输出文件路径
output_file_path = 'output.txt'

key_value_pairs = []

# 小时
max_time = 6


def findSession(ip, port):
    print(f'http://{ip}:{port}/wsman')
    try:
        s = winrm.Session(f'http://{ip}:{port}/wsman', auth=(f'{admin_name}', f'{admin_passwd}'))
        # 执行命令
        r = s.run_cmd('query session')
        # 输出结果
        text = r.std_out.decode()
        if re.search(r"Active", text):
            print("The string contains 'active'.")
            # m.update_status("busy", ip, port)
            # return True
            return "busy"
        else:
            print("The string does not contain 'active'.")
            # resetStatus(ip, port)
            return "free"

    except Exception as e:
        print(e);
        print(f"{ip}:{port}连接异常")
        # m.update_status("error", ip, port)
        return "error"

# 重置密码并设置为空闲，并打上时间标签
def resetStatus(ip, port):
    s = winrm.Session(f'http://{ip}:{port}/wsman', auth=(f'{admin_name}', f'{admin_passwd}'))
    # return False
    m.update_status("free", ip, port)

    # 修改密码为随机数
    newPassword = generate_random_md5();
    editorPassword(ip, port, s, newPassword)
    m.update_passwd(newPassword, ip, port);

    # 获取当前时间,格式化时间为指定格式
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    m.update_resettime(formatted_time, ip, port)


# 生成随机MD5密码
def generate_random_md5():
    # 生成一个随机字符串
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    # 计算MD5哈希值
    return hashlib.md5(random_string.encode()).hexdigest()


def get_remote_powershell_version(session):
    # 发送命令获取PowerShell版本
    ps_script = "($PSVersionTable.PSVersion).ToString()"
    result = session.run_ps(ps_script)

    if result.status_code == 0:
        version_info = result.std_out.decode().strip()
        major, minor = map(int, version_info.split('.')[0:2])
        return major, minor
    else:
        print(f"获取PowerShell版本失败：{result.std_err.decode()}")
        return None


def editorPassword(ip, port, s, password):
    version = get_remote_powershell_version(s)
    print(f'{ip}:{port}PowerShell 版本{version}')
    if version:
        if version < (5, 1):
            # 在这里添加你的逻辑
            ps_script = f"""
            $user = [adsi]"WinNT://./{orgin_username},user"
            $user.SetPassword("{password}")
            """
        else:
            # 使用PowerShell添加用户
            ps_script = f"""
            $Password = ConvertTo-SecureString "{password}" -AsPlainText -Force
            Set-LocalUser -Name "{orgin_username}" -Password $Password
            """
    else:
        print("无法确定 PowerShell 版本或获取失败。")
    r = s.run_ps(ps_script)
    # 输出结果
    # print(r.status_code)
    # print(r.std_out.decode())
    # print(r.std_err.decode())
    if r.status_code == 0:
        # print(f'{orgin_username}成功修改了密码')
        print(f'{ip}:{port}的{orgin_username}用户,新密码为:{password}')


def query_sessions(s, username):
    """查询所有会话，并找到用户名为指定值的会话ID"""
    ps_script = """
    $sessions = quser
    foreach ($session in $sessions[1..($sessions.Length - 1)]) {
        $parts = -split $session.Trim()
        if ($parts[0] -eq '%s') {
            Write-Output $parts[2]
            break
        }
    }
    """ % username
    result = s.run_ps(ps_script)
    if result.status_code == 0:
        session_id = result.std_out.decode().strip()
        return session_id if session_id.isdigit() else None
    else:
        print("Failed to query sessions:", result.std_err.decode())
        return None


def logoff_session(s, session_id):
    """根据会话ID注销指定的会话"""
    if session_id:
        ps_script = f"logoff {session_id}"
        result = s.run_cmd(ps_script)
        if result.status_code == 0:
            print(f'Successfully logged off session {session_id}.')
        else:
            print(f'Failed to logoff session {session_id}:', result.std_err.decode())
    else:
        print('No session found or session ID could not be determined.')


def closeSession(ip, port, username):
    s = winrm.Session(f'http://{ip}:{port}/wsman', auth=(f'{admin_name}', f'{admin_passwd}'))
    # 查询会话ID
    try:
        session_id = query_sessions(s, f'{username}')
        if session_id:
            logoff_session(s, session_id)
        else:
            print(f'Could not find a session for user {username}.')
            print(f'{ip}:{port} 没有操作中会话,无需强制断开')
    except Exception as e:
        print(f'{ip}:{port}winrm服务连接失败')


def parse_time(time_str):
    """解析时间字符串为datetime对象"""
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def checkSession(filename, hour):
    current_time = datetime.now()

    results = m.fetch_and_process_ips();
    # 循环遍历结果并执行逻辑
    for row in results:
        ip = row['ip']
        port = row['mport']
        record_time = row['resettime']
        status = findSession(ip, port)
        m.update_status(status,ip,port)
        if current_time > record_time + timedelta(hours=hour):
            print(f'警告：{ip}:{port}记录时间 {record_time} 超过{hour}小时')
            if status == "busy":
                # 关闭会话
                closeSession(ip, port, orgin_username)
                # 重置状态
                resetStatus(ip, port)
            elif status == "free":
                # 重置状态
                resetStatus(ip, port)
            else:
                print(f'警告：{ip}:{port}目前状态为error,请检测winrm服务');
        else:
            print(f'提示：{ip}:{port}记录时间 {record_time} 未超过{hour}小时')




if __name__ == "__main__":
    print("程序开始运行")
    key_value_pairs = m.fetch_ips();
    # 第一次运行重置密码
    for ip, port in key_value_pairs:
        status = findSession(ip, port)
        if status == "free":
            resetStatus(ip, port)

    while (True):
        # 判断会话是否超过指定时间，如果超过则强制断开并调用resetStatus重置机器
        checkSession(output_file_path, max_time)
        # 睡眠5秒
        time.sleep(5)
