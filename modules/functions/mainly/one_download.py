import re
from modules.utils.inputs import rinput
from modules.functions.mainly.get_song import get_song_lyric
from modules.utils.clear_screen import clear


def download_one_lyric(self):
    """单次下载歌词

    ``path: str`` 存储歌词的路径"""
    clear()
    song_id = rinput(
        f"[NeteaseMusicLyricDownloader] {self.version}\n"
        "[手动-单个下载]\n"
        "请输入歌曲id:")
    try:
        int(song_id)
    except ValueError:
        r = re.search("song\?id=[0-9]*", song_id)
        if r:
            song_id = r.group()[8:]
        else:
            input("不合法的形式.\n按回车键返回...")
            return

    if get_song_lyric(int(song_id), self.settings.lyric_path) == "dl_err_connection":
        input("下载发生错误!可能是连接被拒绝!请检查网络后再试\n按回车键返回...")
    input("按回车键返回...")
