"""集合 下载歌词 以及 获取歌曲信息 的功能"""
import os
from json import loads
from requests import post
from requests.exceptions import ConnectionError
from time import sleep


def wait_retry():
    print("api提示操作频繁，等待恢复...")
    while True:
        try:
            tmp = post(f"http://music.163.com/api/song/detail/?&ids=[1]")
        except ConnectionError:
            return "dl_err_connection"
        else:
            if loads(tmp.text)["code"] == 200:
                return "continue"
        sleep(1)


def get_song_info_raw(types: list, id: str):
    """获取歌曲信息
    
    types 提供一个list,将会返回内部所有符合要求的信息类型\n
    id 提供一个歌曲id(str),将会把歌曲的`types`信息返回"""
    print("id:%s" % id)

    try:
        response = post(f"http://music.163.com/api/song/detail/?&ids=[{id}]")
    except ConnectionError:
        return "dl_err_connection"
    else:
        info = loads(response.text)
        if info["code"] == 406:  # 判断当操作频繁时，继续获取，直到可以返回值为200为止
            result = wait_retry()
            if result == "continue":
                pass
            elif result == "dl_err_connection":
                return "dl_err_connection"
            else:
                raise Exception("Unknown exception...")

        if not info.get("songs"):  # 判断是否存在该歌曲
            print("这首歌没有找到，跳过...")
            return "song_nf"
        else:
            need = {}
            for i in types:  # 通过传入的变量 types 获取信息(根据返回的信息分析得到的下面这句语句)
                need.setdefault(i, info["songs"][0][i])
            return need


def get_song_lyric(id: str | int | dict, path: str, allinfo: bool = False):
    """获取歌词
    
    ``id`` 提供一个歌曲id
    ``path`` 提供歌曲下载的路径
    ``allinfo`` 若此项为 True ,则提供的id格式必须为 {"id": int | str, "name": str, "artists": [[str, ...], ...]} (dict)"""
    if allinfo:
        sinfo = id
        id = id["id"]
    else:
        sinfo = get_song_info_raw(["name", "artists"], id)
        if sinfo == "dl_err_connection":  # 处理各式各样的事件
            return "dl_err_connection"
        elif sinfo == "song_nf":
            return "song_nf"

    # 整理歌曲数据，获取歌词
    artists = ""
    if allinfo:
        for i in sinfo["artists"]:
            artists += f"{i[0]},"
    else:
        for i in sinfo["artists"]:
            artists += f"{i['name']},"
    artists = artists[:-1]

    name = sinfo["name"]
    if not name:
        print("歌曲错误!这是网易云的问题,请不要找作者")
        return "song_err"
    replaces = {  # 处理非法字符所用的替换字典(根据网易云下载的文件分析得到)
        "|": "｜",
        ":": "：",
        "<": "＜",
        ">": "＞",
        "?": "？",
        "/": "／",
        "\\": "＼",
        "*": "＊",
        '"': "＂"
    }
    for k, v in replaces.items():
        name = name.replace(k, v)
        artists = artists.replace(k, v)

    print(f"歌曲:{name} - {artists}")
    filename = f"{name} - {artists}.lrc"

    try:
        response = post(f"http://music.163.com/api/song/media?id={id}")
    except ConnectionError:
        return "dl_err_connection"
    else:
        info = loads(response.text)
        if info["code"] == 406:  # 此处与上方一样，防止因为请求限制而跳过下载
            result = wait_retry()
            if result == "continue":
                pass
            elif result == "dl_err_connection":
                return "dl_err_connection"
            else:
                raise Exception("Unknown exception...")

    tmp = loads(response.text)
    if tmp.get("nolyric") or not tmp.get('lyric'):
        print("这首歌没有歌词，跳过...")
        return
    else:
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write(tmp["lyric"])
        print(f"歌词下载完成!被保存在{os.path.join(path, filename)}")
        return
