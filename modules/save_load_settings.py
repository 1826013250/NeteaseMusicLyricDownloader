"""加载 or 保存设置文件"""

import json
import os


class Settings(object):  # 设定一个基础的存储设置信息的 class
    def __init__(self, l_p="./out/", lang="en"):
        self.lyric_path = l_p
        self.language = lang


def class2dict(aclass):  # 让 json.dumps 将 class 转化为一个 dict ,用于保存
    return {
        "lyric_path": aclass.lyric_path,
        "language": aclass.language,
    }


def dict2class(adict):  # 让 json.load 将读取到的 dict 转化为我们所需要的 class
    if len(adict) != 2:  # 若检测到多余的设定将抛出异常
        raise json.decoder.JSONDecodeError("Too many keys", "none", 0)
    else:
        return Settings(adict["lyric_path"], adict["language"])


def load_settings():  # 加载 的函数
    """加载设置
    调用即可，无需参数
    返回: 设置 class"""
    if os.path.exists("settings.json"):  # 判断目录下是否存在 settings.json ,若没有则创建,若有则读取
        with open("settings.json", 'r', encoding="utf-8") as f:
            try:
                return json.load(f, object_hook=dict2class)
            except json.decoder.JSONDecodeError:  # 如果检测到文件无法读取,将会删除设置文件并重新创建
                print("设置文件损坏,重新创建...")
                os.remove("settings.json")
                return load_settings()
    else:
        with open("settings.json", 'w', encoding="utf-8") as f:
            f.write(json.dumps(Settings(), default=class2dict))
            return Settings()


def save_settings(settings):  # 保存 的函数
    """保存设置
    ``settings`` 传入一个 设置 class 将其序列化为json
    返回 done 即为完成，理论上不存在报错所以暂时没有做其他处理"""
    with open("settings.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(settings, default=class2dict))
        input("保存完成!按回车继续...")
