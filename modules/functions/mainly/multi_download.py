import re
from colorama import Fore

from modules.utils.clear_screen import cls_stay
from modules.utils.inputs import rinput
from modules.functions.mainly.download_multiple_songs import donload_multiple_songs


def mdl(self):
    """多个歌词文件的下载

    ``path: str`` 传入歌词文件保存的路径"""
    cls_stay(self, "[手动-多个下载]")
    ids = []
    print("输入歌曲id,用回车分开,输入s停止")
    while True:
        r = rinput()
        if r == 's':
            break
        else:
            try:
                int(r)
            except ValueError:
                tmp = re.search(r"song\?id=[0-9]*", r)
                if tmp:
                    r = tmp.group()[8:]
                else:
                    print("不合法的形式.\n")
                    continue
            ids.append(int(r))
            print("\t#%d id:%s - 已添加!" % (len(ids), r))
    cls_stay(self, "[手动-多个下载]")
    donload_multiple_songs(self, self.settings.lyric_path, ids)

    input("按回车键返回...")
