# backend

1. conda的安装可参考[超详细的linux-conda环境安装教程](https://blog.csdn.net/Alex_81D/article/details/135692506)



2. 将后端仓库克隆到本地

   ```bash
   git clone https://github.com/HarmonyAgriLab/backend.git
   ```



3. 创建虚拟环境并指定python版本

   ```bash
   conda create -n your_conda_env_name python=3.12
   ```



4. 激活创建的虚拟环境

   ```bash
   conda activate your_conda_env_name
   ```



5. 安装所需库

   ```bash
   pip install -r requirements.txt
   ```



6. 启动后端服务

   ```bash
   python server.py
   ```



7. 启动订阅服务

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
