"""集合 下载歌词 以及 获取歌曲信息 的功能"""
import os
from requests import post
from requests.exceptions import ConnectionError
from time import sleep
from colorama import Fore, Style

from modules.utils.bar import CompactBar, bprint
from modules.utils.dump import regular_filename


def wait_retry(kind, identify, bar=None):
    bprint("api提示操作频繁，等待恢复...", bar)
    if kind == "information":
        url = f"https://music.163.com/api/song/detail/?&ids=[{identify}]"
    elif kind == "lyric":
        url = f"https://music.163.com/api/song/media?id={identify}"
    else:
        return "unknown_kind"
    while True:
        try:
            tmp = post(url).json()
        except ConnectionError:
            return "dl_err_connection"
        else:
            if tmp["code"] == 200:
                return tmp
        sleep(1)


def get_song_info_raw(types: list, identify: str, bar: CompactBar = None):
    """获取歌曲信息
    
    ``types`` 提供一个list,将会返回内部所有符合要求的信息类型\n
    ``identify`` 提供一个歌曲id(str),将会把歌曲的`types`信息返回"""
    bprint(Fore.CYAN + "ID:%s" % identify, bar)

    try:
        info = post(f"https://music.163.com/api/song/detail/?&ids=[{identify}]").json()
    except ConnectionError:
        return "dl_err_connection"
    else:
        if info["code"] == 406:  # 判断当操作频繁时，继续获取，直到可以返回值为200为止
            result = wait_retry("information", identify, bar=bar)
            if type(result) == dict:
                info = result
            elif result == "dl_err_connection":
                return "dl_err_connection"
            else:
                raise Exception("Unknown exception...")

        if not info.get("songs"):  # 判断是否存在该歌曲
            bprint(Fore.LIGHTBLACK_EX + "\t-> 这首歌没有找到，跳过...", bar)
            return "song_nf"
        else:
            need = {}
            for i in types:  # 通过传入的变量 types 获取信息(根据返回的信息分析得到的下面这句语句)
                need.setdefault(i, info["songs"][0][i])
            return need


def get_song_lyric(identify: str | int | dict, path: str, allinfo: bool = False, bar: CompactBar = None):
    """获取歌词
    
    ``identify`` 提供一个歌曲id
    ``path`` 提供歌曲下载的路径
    ``allinfo`` 若此项为 True ,则提供的identify格式必须为存储在网易云下载文件中meta_data的格式
    ``bar`` 若获取歌词时下方有进度条, 则应当传入此参数"""
    if allinfo:
        sinfo = identify
        identify = identify["id"]
        bprint(Fore.CYAN + f"ID: {identify}", bar)
    else:
        sinfo = get_song_info_raw(["name", "artists"], identify, bar)
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
        bprint(Fore.RED + "歌曲错误!这是网易云的问题,请不要找作者", bar)
        return "song_err"

    name = regular_filename(name)
    artists = regular_filename(artists)

    bprint(Fore.YELLOW + "\t-> 歌曲:" + Style.RESET_ALL + f"{name} - {artists}", bar)
    filename = f"{name} - {artists}.lrc"

    try:
        info = post(f"https://music.163.com/api/song/media?id={identify}").json()
    except ConnectionError:
        return "dl_err_connection"
    else:
        if info["code"] == 406:  # 此处与上方一样，防止因为请求限制而跳过下载
            result = wait_retry("lyric", identify, bar=bar)
            if type(result) == dict:
                info = result
            elif result == "dl_err_connection":
                return "dl_err_connection"
            else:
                raise Exception("Unknown exception...")

    if info.get("nolyric") or not info.get('lyric'):
        bprint(Fore.LIGHTBLACK_EX + "\t--> 这首歌没有歌词，跳过...\n", bar)
        return
    else:
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            f.write(info["lyric"])
        bprint(Fore.GREEN + "\t--> 歌词下载完成!被保存在" + Style.RESET_ALL + f"{os.path.join(path, filename)}\n", bar)
        return
