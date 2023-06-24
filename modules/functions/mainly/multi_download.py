import re
from colorama import Fore

from modules.utils.clear_screen import cls_stay
from modules.utils.inputs import rinput
from modules.functions.mainly.get_song import get_song_lyric
from modules.utils.bar import CompactArrowBar


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
    with CompactArrowBar(f"进度: %(index){len(str(len(ids)))}d/%(max)d",
                         suffix="", max=len(ids), color="yellow", width=9999) as bar:
        for i in range(0, len(ids)):
            r = get_song_lyric(ids[i], self.settings.lyric_path, self.settings.lyric_path, bar=bar)
            if r == "dl_err_connection":
                bar.print_onto_bar(Fore.RED + "下载发生错误！可能是连接被拒绝!请检查网络后再试\n按回车键继续任务(该任务会被跳过)...")
                input()
            bar.next()
    input("按回车键返回...")
