# violin

### 安装virtualenv

```shell
pip3 install virtualenv
```

### 创建目录

```shell
mkdir violin
cd violin
```

### 创建虚拟环境

```shell
virtualenv env
```

### 激活虚拟环境

```shell
# windows
env\Scripts\activate
# linux
source env/bin/activate
```

### 生成爬虫项目框架

```shell
pip3 install scrapy
scrapy startproject violin_scraper
```

### 安装ChromeDriver

1. 首先下载chromedriver
下载地址：http://chromedriver.storage.googleapis.com/index.html

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
