# violin

### 安装virtualenv

```shell
$ pip3 install virtualenv
```

### 创建目录

```shell
$ mkdir violin
$ cd violin
```

### 创建虚拟环境

```shell
$ virtualenv env
```

### 激活虚拟环境

```shell
# windows
$ env\Scripts\activate
# linux
$ source env/bin/activate
```

### 生成爬虫项目框架

```shell
$ pip3 install scrapy
$ scrapy startproject violin_scraper
```

### 安装ChromeDriver

1. 首先下载chromedriver
下载地址：<http://chromedriver.storage.googleapis.com/index.html>

2. 查看自己chrome浏览器版本

3. 将下载下来的文件解压，把chromedriver放在chrome安装目录下

- Windows

`C:\Program Files (x86)\Google\Chrome\Application`

- Ubantu

i. Check if google-chrome has been installed

```shell
which google-chrome
```

ii. Check if ChromeDriver has been installed

```shell
which ChromeDriver
```

iii. Copy unziped chromeDriver file to `/usr/bin folder`

iv. Verify if ChromeDriver works

```shell
chromedriver
```

4. 配置环境变量，加入到PATH中。

### 安装Docker

### 安装Redis

1. 查找Docker Hub上的redis镜像

```shell
$ docker search redis
```

2. 选取当前最新的6.0.5进行拉取

```shell
$ docker pull redis:6.0.5
# docker pull redis:latest
```

3. 创建要挂在的文件夹

#### Windows

```bat
md \mydata\redis\data
md \mydata\redis\conf
md \mydata\redis\log
echo 2> \mydata\redis\conf\redis.conf
```

> 被映射到windows系统中的log文件，无法识别\r, 所以无法换行

#### Linux

```shell
$ mkdir -p /mydata/redis/data
$ mkdir -p /mydata/redis/conf
$ mkdir -p /mydata/redis/log
$ touch /mydata/redis/conf/redis.conf
```

4. 运行容器

#### Windows

```bat
docker run ^
--name single-redis ^
-p 6379:6379 ^
-v /c/mydata/redis/data:/data:rw ^
-v /c/mydata/redis/conf/redis.conf:/etc/redis/redis.conf:rw ^
-v /c/mydata/redis/log:/redislog:rw ^
--privileged=true ^
-d redis:6.0.5 redis-server /etc/redis/redis.conf --requirepass mypass 
```

#### Linux

```shell
$ docker run \
--name single-redis \ # 容器名
-p 6379:6379 \ # 端口映射 宿主机:容器
-v /mydata/redis/data:/data:rw \ # 映射数据目录 rw为读写
-v /mydata/redis/conf/redis.conf:/etc/redis/redis.conf:rw \ # 挂载配置文件
-v /mydata/redis/log:/redislog:rw \
--privileged=true \ # 赋予容器内root权限
--requirepass mypass \ # 设置默认密码
-d redis:6.0.5 redis-server /etc/redis/redis.conf # deamon启动，服务使用指定的配置文件
```

5. 常用命令

#### 进入容器调试

```shell
$ docker exec -it {container-id} or {container-name} bash
```

#### 打开redis-cli

方法一, 在`bash`中打开, 进入容器调试后

```shell
$ cd /usr/local/bin
$ redis-cli
```

方法二, 直接打开`redis-cli`

```shell
$ docker exec -it {container-id} or {container-name} redis-cli
```

#### 在远程服务器上执行命令

```shell
$ redis-cli -h {host} -p {port} -a {password}
```

例如：

```shell
$ redis-cli -h 127.0.0.1 -p 6379 -a "mypass"
redis 127.0.0.1:6379>
redis 127.0.0.1:6379> PING

PONG
```

#### 密码设置

为现有的redis创建密码或修改密码

i. 进入redis的容器`docker exec -it {container-id} redis-cli`

ii. 查看现在的redis密码: `config get requirepass`

iii. 设置redis密码：`config set requirepass {password}`

iv. 若出现`(error)NOAUTH Authentication required.`错误，则使用`auth {password}`来认证密码
