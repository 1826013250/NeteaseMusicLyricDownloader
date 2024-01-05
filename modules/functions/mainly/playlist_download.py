import re
from modules.utils.inputs import rinput
from modules.functions.mainly.get_playlist import getplaylist
from modules.utils.clear_screen import clear
from modules.functions.mainly.download_multiple_songs import donload_multiple_songs
from os.path import sep
from modules.utils.initapp import mkdir

def download_by_playlist(self) -> None:
    """
    按照歌单id获取歌词

    :params: path: str 存储歌词的路径

    :return: None

    """
    clear()
    playlist_id = rinput(
        f"[NeteaseMusicLyricDownloader] {self.version}\n"
        "[手动-歌单下载]\n"
        "请输入歌曲id:")
    try:
        int(playlist_id)
    except ValueError:
        r = re.search("playlist\?id=[0-9]*", playlist_id)
        if r:
            playlist_id = r.group()[12:]
        else:
            input("不合法的形式.\n按回车键返回...")
            return

    playlist = getplaylist(playlist_id)

    if not playlist["playlist"]:
        print("改歌单为空集,下载停止!")
        input()
        return

    if mkdir(self.settings.lyric_path+sep+playlist["name"]):
        print("歌单文件夹已存在")

    donload_multiple_songs(self, self.settings.lyric_path+sep+playlist["name"], playlist["playlist"])
    input("按回车键返回...")

