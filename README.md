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