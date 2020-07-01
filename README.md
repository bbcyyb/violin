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

### 安装Docker Desktop for Windows

需要`Windows 10 Professional 64-bit`以上版本

#### Install

Double-click `Docker for Windows Installer` to run the installer.

When the installation finishes, Docker starts automatically. The whale in the notification area indicates that Docker is running, and accessible from a terminal.

#### Run

Open a command-line terminal like PowerShell, and try out some Docker commands!

Run `docker version` to check the version.

Run `docker run hello-world` to verify that Docker can pull and run images.

#### Enjoy

Docker is available in any terminal as long as the Docker Desktop for Windows app is running. Settings are available on the UI, accessible from the Docker whale in the taskbar.