from colorama import Fore

from modules.utils.bar import CompactArrowBar
from modules.functions.mainly.get_song import get_song_lyric

def donload_multiple_songs(self, lyric_path: str, ids):
    with CompactArrowBar(f"进度: %(index){len(str(len(ids)))}d/%(max)d",
                         suffix="", max=len(ids), color="yellow", width=9999) as bar:
        for i in range(0, len(ids)):
            print(ids[i])
            r = get_song_lyric(ids[i], lyric_path, self.settings.lyric_format, bar=bar, save_lyrics_time = self.settings.save_lyrics_time)
            if r == "dl_err_connection":
                bar.print_onto_bar(Fore.RED + "下载发生错误！可能是连接被拒绝!请检查网络后再试\n按回车键继续任务(该任务会被跳过)...")
                input()
            bar.next()
