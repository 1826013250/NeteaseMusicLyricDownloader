# NeteaseMusicLyricDownloader
[English](https://github.com/1826013250/NeteaseMusicLyricDownloader)|**简体中文**

一个下载网易云音乐歌词的简单工具

## 这个玩意原理是啥?
它用了Python中的一个`requests`模块来实现抓取歌词文件的功能

网易云音乐提供给我们了一个获取歌词的API ~~然后我就做了这个程序（~~

## 爷要安装
首先，你需要一个Python环境(要求版本>=3.10,因为使用了3.10python的新特性)，然后使用pip来安装`requests` `mutagen` `pycryptodomex`这几个包
>您觉得很麻烦?_~~事真多~~_ 直接复制这段命令到终端罢！（你得先有Python和pip）： `python3 -m pip install requests mutagen pycryptodomex`

然后，把整个项目薅下来，在当前目录下运行`python3 main.py`就行了

## 这玩意到底能干啥?
~~nmd~~这玩意就像它的名字一样，下载歌词用的

你需要提供歌曲的id或者分享链接，然后这破玩意就会自动下载歌词

啊现在，它可以识别网易云音乐客户端下载的音乐了（识别内部的163 key），484更舒服了？

- 2022/8/13 啊现在啊现在, 它集成了ncmdump的功能, 可以识别网易云的加密文件格式,解密并获取歌词!真实令人激动的新功能啊!!

## 后续有啥功能？

_~~我不造，要不你来写罢（~~_

## 其他要说的

这就一简简单单普普通通的程序

我可能也没有太多的精力去写这么个~~破玩意~~...
