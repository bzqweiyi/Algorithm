# 基于Scrapy的Python3分布式爬虫
* Items.py : 定义爬取的数据
* pipelines.py : 后处理(Post-process)，存储爬取的数据
* taobao.py : 爬虫程序
* settings.py : Srapy设定，请参考 [内置设定参考手册 ](https://scrapy-chs.readthedocs.io/zh_CN/latest/topics/settings.html#topics-settings-ref)


##  使用教程：
#### 1. 运行前你需要安装并配置好环境：
* Python3
* Scrapy
* MongoDB
* redis

#### 2. 打开MongoDB和redis服务
#### 3. 下载并解压
#### 4. 打开多个cmd，把路径都切换到corpus目录下，输入 *scrapy crawl 爬虫名称*
#### 5. 打开cmd，把路径切换到redis目录下，提交start_url，例如：
```cmd
C:\Users>d:

D:\>cd redis

D:\Redis>redis-cli

127.0.0.1:6379> LPUSH jbk39net:start_urls http://jbk.39.net
```
#### 6. 在终端中可看见爬取过程，数据存储在MangoDB的tbdb库的表中（存储位置可在pipelines.py中修改）

#### 7. 程序结束后，清除redis中的缓存
```cmd
127.0.0.1:6379> flushdb
```
