# backend

1. conda的安装可参考[超详细的linux-conda环境安装教程](https://blog.csdn.net/Alex_81D/article/details/135692506)



2. emqx部署可参考[部署 EMQX](https://docs.emqx.com/zh/emqx/latest/deploy/install-ubuntu.html)



3. 将后端仓库克隆到本地

   ```bash
   git clone https://github.com/HarmonyAgriLab/backend.git
   ```



4. 创建虚拟环境并指定python版本

   ```bash
   conda create -n your_conda_env_name python=3.12
   ```



5. 激活创建的虚拟环境

   ```bash
   conda activate your_conda_env_name
   ```



6. 安装所需库

   ```bash
   pip install -r requirements.txt
   ```



7. 后端配置文件config.yaml文件说明

```yaml
mysql: # mysql配置
        host: 127.0.0.1 # 本地主机
        port: ****** # 配置为mysql默认端口：3306
        username: root # 用户名，本地登录可用root，远程登录可用user
        password: ****** # 需要配置为用户的对应密码！！！
        database: ****** # 配置使用的数据库：emqx

emqx: # emqx订阅发布配置
        username: user # 用户名，可用root或user
        password: ****** # 需要配置为用户的对应密码！！！
        topic: /Agriculture/# # 配置监听主题
        broker: 127.0.0.1 # 配置mqtt服务端
        port: ****** # 配置mqtt协议默认端口：1883
```





8. 启动后端服务

   ```bash
   python server.py
   ```



9. 启动订阅服务

   ```bash
   python subscribe.py
   ```

   

#### 数据库(mysql)简介：

mysql  Ver 8.0.41-0ubuntu0.20.04.1 for Linux on x86_64 ((Ubuntu))
Current database:	emqx
Current user:	root@localhost / user@%
Using delimiter:	;
Server version:	8.0.41-0ubuntu0.20.04.1 (Ubuntu)
Protocol version:	10
Server characterset:	utf8mb4
Db characterset:	utf8mb4
Client characterset:	utf8mb4
Conn.characterset:	utf8mb4
UNIX socket:	/var/run/mysqld/mysqld.sock
Binary data as:	Hexadecimal
