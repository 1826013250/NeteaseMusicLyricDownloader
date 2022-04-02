# 导入自定义模块使用try，原因是如果在外部单独运行文件，无法通过modules索引到依赖的模块
# 直接单独运行会出现 ModuleNotFoundError 报错

from modules.raw_input import rinput
from modules.get_song import get_song_lyric
from modules.clear_screen import clear


def download_one_lyric(path: str):
    """单次下载歌词

    ``path: str`` 存储歌词的路径"""
    clear()
    song_id = rinput("请输入歌曲id:")
    try:
        int(song_id)
    except ValueError:
        input("不合法的id形式.\n按回车键返回...")
    else:
        if get_song_lyric(song_id, path) == "dl_err_connection":
            input("下载发生错误!可能是连接被拒绝!请检查网络后再试\n按回车键返回...")
        input("按回车键返回...")
