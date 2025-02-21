import mysql.connector
from datetime import datetime


def getConection():
    connection = mysql.connector.connect(
        host='218.93.208.157',  # 数据库IP地址
        user='root',  # 替换为你的用户名
        password='',  # 替换为你的密码
        database='winmanage',  # 数据库名
        port=3307  # 端口号
    )
    return connection


def fetch_ips():
    try:
        # 创建数据库连接
        connection = getConection()

        # 创建游标对象
        cursor = connection.cursor()

        # SQL查询语句
        query = "SELECT ip, mport FROM ips"

        # 执行SQL语句
        cursor.execute(query)

        # 获取所有结果
        results = cursor.fetchall()

        # 将结果转换为目标格式
        formatted_results = [(result[0], result[1]) for result in results]

        return formatted_results

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")
        return []

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")


# 调用函数并打印结果
# ips_list = fetch_ips()
# print(ips_list)


def update_status(status, ip, mport):
    try:
        # 创建数据库连接
        connection = getConection()

        # 创建游标对象
        cursor = connection.cursor()

        # SQL更新语句
        query = "UPDATE ips SET status = %s WHERE ip = %s AND mport = %s"

        # 执行SQL语句
        cursor.execute(query, (status, ip, mport))

        # 提交更改到数据库
        connection.commit()

        # print(f"Record updated successfully for IP: {ip}, MPort: {mport}")

    except mysql.connector.Error as error:
        print(f"Failed to update record to MySQL: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# 示例调用函数
# update_status('active', '218.93.208.157', 5985)


def update_passwd(newpasswd, ip, mport):
    try:
        # 创建数据库连接
        connection = getConection()

        # 创建游标对象
        cursor = connection.cursor()

        # SQL更新语句
        query = "UPDATE ips SET passwd = %s WHERE ip = %s AND mport = %s"

        # 执行SQL语句
        cursor.execute(query, (newpasswd, ip, mport))

        # 提交更改到数据库
        connection.commit()

        # print(f"Record updated successfully for IP: {ip}, MPort: {mport}")

    except mysql.connector.Error as error:
        print(f"Failed to update record to MySQL: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")


# update_passwd('dsafdsfa', '218.93.208.157', 5985)


def update_resettime(datetime_value, ip, mport):
    try:
        # 创建数据库连接
        connection = getConection()

        # 创建游标对象
        cursor = connection.cursor()

        # SQL更新语句
        query = "UPDATE ips SET resettime = %s WHERE ip = %s AND mport = %s"

        # 将字符串转换为datetime对象，如果需要的话
        if isinstance(datetime_value, str):
            datetime_obj = datetime.strptime(datetime_value, '%Y-%m-%d %H:%M:%S')
        else:
            datetime_obj = datetime_value

        # 执行SQL语句
        cursor.execute(query, (datetime_obj, ip, mport))

        # 提交更改到数据库
        connection.commit()

        # print(f"Record updated successfully for IP: {ip}, MPort: {mport}")

    except mysql.connector.Error as error:
        print(f"Failed to update record to MySQL: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")


# current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# update_resettime(current_time, '218.93.208.157', 5985)


def fetch_and_process_ips():
    try:
        # 创建数据库连接
        connection = getConection()

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # 使用字典游标方便访问列名
            query = "SELECT ip, mport, status, resettime FROM ips"

            # 执行SQL语句
            cursor.execute(query)

            # 获取所有结果
            results = cursor.fetchall()
            return results

    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")
