可以通过SQLyog直接修改用户权限，以下是详细步骤：
方案一：通过SQLyog图形界面操作
```SQL

-- 1. 用SQLyog登录后打开查询窗口，执行以下SQL（注意替换密码）
ALTER USER 'ZHANG3'@'localhost' 
IDENTIFIED WITH mysql_native_password BY '你的新密码';

-- 2. 刷新权限
FLUSH PRIVILEGES;

-- 3. 检查用户权限（可选）
SELECT user, host, plugin FROM mysql.user;
```
方案二：检查MySQL服务状态（关键步骤）
```BASH

# 先确认MySQL服务是否真的在运行
# Windows查看服务状态（管理员权限）
sc query mysql

# Linux检查服务状态
systemctl status mysql

# 如果服务未运行，需先启动服务
net start mysql  # Windows
sudo systemctl start mysql  # Linux
```
方案三：通过SQLyog重置root密码（备用方案）

    在SQLyog中新建一个查询窗口
    执行：

```SQL

ALTER USER 'root'@'localhost' IDENTIFIED BY '新密码';
```
方案四：强制修改配置文件（终极手段）

    找到my.ini/my.cnf文件（通常位于C:\ProgramData\MySQL\MySQL Server 8.0或/etc/mysql）
    在[mysqld]段添加：

```INI

skip-grant-tables
skip-networking
```
    重启MySQL服务后即可无密码登录

连接参数优化建议（Java程序）
```JAVA

// 在JDBC URL后添加这两个参数
jdbc:mysql://127.0.0.1:3306/dbname?
  useSSL=false&
  allowPublicKeyRetrieval=true
```
关键检查点清单

    ✅ 确认MySQL服务状态（运行中/已停止）
    ✅ 检查用户是否存在双重账户（'ZHANG3'@'localhost'和'ZHANG3'@'%'）
    ✅ 验证密码是否包含特殊字符（建议暂时使用纯字母数字密码）
    ✅ 查看错误日志（Windows：C:\ProgramData\MySQL\MySQL Server 8.0\Data\主机名.err）

通过SQLyog执行这些操作后，建议重启MySQL服务并尝试用命令行重新连接。如果仍然失败，可通过`SHOW VARIABLES LIKE 'validate_password%';`查看密码策略强度。
