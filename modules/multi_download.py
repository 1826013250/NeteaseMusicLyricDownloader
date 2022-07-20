import re
from modules.clear_screen import clear
from modules.raw_input import rinput
from modules.get_song import get_song_lyric


def mdl(path: str):
    """多个歌词文件的下载

    ``path: str`` 传入歌词文件保存的路径"""
    clear()
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
            ids.append(r)
            print("\t#%d id:%s - 已添加!" % (len(ids), r))
    clear()
    for i in range(0, len(ids)):
        print("\n进度: %d/%d" % (i+1, len(ids)))
        if get_song_lyric(ids[i], path) == "dl_err_connection":
            input("下载发生错误！可能是连接被拒绝!请检查网络后再试\n按回车键继续任务(该任务会被跳过)...")
    input("按回车键返回...")
