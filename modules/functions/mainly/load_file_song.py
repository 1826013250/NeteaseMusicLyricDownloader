import json
import os
from base64 import b64decode
from multiprocessing import Process, Queue
from queue import Empty
from time import sleep
from sys import exit

import mutagen.mp3
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

from mutagen import File
from colorama import Fore, Style

from modules.utils.clear_screen import cls_stay
from modules.functions.mainly.get_song import get_song_lyric
from modules.utils.inputs import cinput, rinput
from modules.utils.bar import CompactBar, CompactArrowBar
from modules.utils.dump import load_and_decrypt_from_ncm


def load_information_from_song(path) -> str | dict:
    """从音乐文件中的 Comment 字段获取 163 key 并解密返回歌曲信息"""
    try:
        file = File(path)  # 使用 mutagen 获取歌曲信息
    except mutagen.mp3.HeaderNotFoundError:
        return "not_a_music"
    if os.path.splitext(path)[-1] == ".mp3":  # 当文件为 mp3 时使用 ID3 格式读取
        if file.tags and file.tags.get("COMM::XXX"):
            if file.tags["COMM::XXX"].text[0][:7] == "163 key":
                ciphertext = file.tags["COMM::XXX"].text[0][22:]
            else:
                return "not_support"
        else:
            return "not_support"
    elif os.path.splitext(path)[-1] == ".flac":  # 当文件为 flac 时使用 FLAC 格式读取
        if file.tags.get("DESCRIPTION"):
            if file.tags["DESCRIPTION"][0][:7] == "163 key":
                ciphertext = file.tags["DESCRIPTION"][0][22:]
            else:
                return "not_support"
        else:
            return "not_support"
    else:
        return "not_support"

    cryptor = AES.new(b"#14ljk_!\\]&0U<'(", AES.MODE_ECB)  # 使用密钥创建解密器

    # 下方这一行将密文 ciphertext 转换为 bytes 后进行 base64 解码, 得到加密过的 AES 密文
    # 再通过上方创建的 AES 128-ECB 的解密器进行解密, 然后使用 unpad 清除末尾无用的占位符后得到结果
    try:
        r = unpad(cryptor.decrypt(b64decode(bytes(ciphertext, "utf-8"))), 16).decode("utf-8")
    except ValueError:
        return "decrypt_failed"

    if r:
        if r[:5] == "music":
            return json.loads(r[6:])
        else:
            return "not_a_normal_music"
    else:
        return "decrypt_failed"


def process_work(path, filename, target, lyric_format, q_err: Queue, q_info: Queue):
    try:
        result = load_and_decrypt_from_ncm(path, target, lyric_format)
    except AssertionError:
        q_err.put(f"\t- 文件 \"{filename}\" 破解失败!")
    except KeyboardInterrupt:
        os.remove(target)
        exit(-1)
    else:
        if result == "no_meta_data":
            q_err.put(f"\t- 文件 \"{filename}\"破译成功, 但是未发现有效的歌曲信息, 将不会下载该歌词")
        q_info.put(result)


def get_lyric_from_folder(self):
    cls_stay(self, "[自动获取 - 加载文件]")
    path = cinput("请输入歌曲的保存文件夹(绝对路径):")
    if not os.path.exists(path):
        input("路径不存在.\n按回车返回...")
        return

    print("正在遍历目录,请稍后...")
    musics = []
    ncm_files = []
    fails = 0
    for i in os.listdir(path):  # 遍历目录,查找目标文件
        ext = os.path.splitext(i)[-1]
        if ext in ['.mp3', '.flac']:  # 对于 mp3 和 flac 文件, 使用对应读取解密方式
            result = load_information_from_song(os.path.join(path, i))
            if result == "not_support":
                fails += 1
                print(f"文件 \"{i}\" 未包含 163 key ,跳过")
            elif result == "decrypt_failed":
                fails += 1
                print(f"文件 \"{i}\" 内 163 key 解密失败,跳过")
            elif result == "not_a_normal_music":
                fails += 1
                print(f"文件 \"{i}\" 内 163 key 不是一个普通音乐文件,这可能是一个电台曲目")
            elif result == "not_a_music":
                fails += 1
                print(f"文件 \"{i}\" 不是一个音乐文件,请检查该文件是否正常")
            else:
                musics.append({"id": result['musicId'], "name": result["musicName"], "artists": result["artist"]})
        elif ext == ".ncm":  # 对于 ncm 先加入到列表，等待解密
            ncm_files.append(i)
        else:
            pass

    target_path = ""
    if ncm_files:
        while True:
            print(f"\n发现{len(ncm_files)}个ncm加密文件!")
            print("请问解密后的文件保存在哪里?\n"
                  "[1] 保存在相同文件夹内\n"
                  "[2] 保存在程序设定的下载文件夹中\n"
                  "[3] 保存在自定义文件夹内\n"
                  "[q] 取消解密,下载歌词时将忽略这些文件")
            select = rinput("请选择: ")
            if select == 'q':
                target_path = "NOT_DECRYPT"
                break
            elif select == '1':
                target_path = path
                break
            elif select == '2':
                target_path = self.settings.lyric_path
                break
            elif select == '3':
                target_path = cinput("请输入: ")
                break
            else:
                print("输入无效！按回车继续...")

        if target_path != "NOT_DECRYPT":  # 开始进行逐个文件解密
            errors = []  # 初始化变量
            q_err = Queue()  # 错误信息队列
            q_info = Queue()  # 返回信息队列
            max_process = 20  # 最大进程数
            current_process = 0  # 当前正在活动的进程数
            passed = 0  # 总共结束的进程数
            with CompactArrowBar(f"正在解锁 %(index){len(str(len(ncm_files)))}d/%(max)d",
                                 suffix="", max=len(ncm_files), color="green", width=9999) as bar:
                total = len(ncm_files)
                allocated = 0  # 已经分配的任务数量
                while True:  # 进入循环，执行  新建进程->检测队列->检测任务完成  的循环
                    sleep(0.05)
                    if current_process <= max_process and allocated < total:  # 分配进程
                        Process(target=process_work,
                                args=(os.path.join(path, ncm_files[allocated]),
                                      ncm_files[allocated],
                                      target_path,
                                      self.settings.lyric_format,
                                      q_err,
                                      q_info)).start()
                        bar.print_onto_bar(Fore.CYAN + "已分配: " + Style.RESET_ALL + "%s" % ncm_files[allocated])
                        allocated += 1
                        current_process += 1
                    while True:  # 错误队列检测
                        try:
                            errors.append(q_err.get_nowait())
                            passed += 1  # 总任务完成数
                            current_process -= 1  # 检测到进程完毕将进程-1
                            bar.next()  # 推动进度条
                            fails += 1  # 错误数量+1
                        except Empty:
                            break
                    while True:  # 信息队列检测
                        try:
                            r = q_info.get_nowait()
                            musics.append({"id": r['musicId'], "name": r["musicName"], "artists": r["artist"]})
                            passed += 1
                            current_process -= 1
                            bar.print_onto_bar(Fore.YELLOW +
                                               f"\"{r['musicName']} - "
                                               f"{''.join([x + ', ' for x in [x[0] for x in r['artist']]])[:-2]}"
                                               "\"" + Fore.GREEN + " 已完成!")
                            bar.next()
                        except Empty:
                            break
                    if passed >= len(ncm_files):
                        break
            if errors:
                print(Fore.LIGHTRED_EX+"解锁过程中发现了以下错误:")
                for i in errors:
                    print(i)

    # 汇报索引结果
    ncm_files_num = 0
    if ncm_files:
        if target_path == "NOT_DECRYPT":
            ncm_files_num = len(ncm_files)
    print(f"\n索引完毕!共找到{fails + len(musics) + ncm_files_num}个目标文件\n{len(musics)}个文件已载入\n{fails}个文件失败")
    if ncm_files:
        if target_path == "NOT_DECRYPT":
            print(f"{len(ncm_files)}个文件放弃加载")
    while True:
        print("\n你希望如何保存这些歌曲的歌词?\n[1]保存到刚刚输入的绝对路径中\n[2]保存到程序设定的下载路径中")
        r = rinput("请选择: ")
        if r == "1":
            lyric_path = path
            break
        elif r == "2":
            lyric_path = self.settings.lyric_path
            break
        else:
            try:
                input("无效选择, 若取消请按 ^C ,继续请按回车")
            except KeyboardInterrupt:
                return

    cls_stay(self, "[自动获取 - 下载歌词]")
    with CompactArrowBar(f"进度: %(index){len(str(len(musics)))}d/%(max)d",
                         suffix="", max=len(musics), color="yellow", width=9999) as bar:
        for i in range(0, len(musics)):  # 根据索引结果获取歌词
            if get_song_lyric(musics[i], lyric_path, self.settings.lyric_format, True, bar) == "dl_err_connection":
                bar.print_onto_bar(Fore.RED + "下载发生错误！可能是连接被拒绝!请检查网络后再试\n按回车键继续任务(该任务会被跳过)...")
                input()
            bar.next()
    if ncm_files:
        if target_path != "NOT_DECRYPT":
            agree = rinput(Fore.RED + "是否删除原ncm文件? (y/n)")
            if agree == "y":
                for i in range(0, len(ncm_files)):
                    print("删除进度: %d/%d\n -> %s\033[F" % (i + 1, len(ncm_files), ncm_files[i]), end="")
                    os.remove(os.path.join(path, ncm_files[i]))
            else:
                print("取消.", end="")
    input("\n\033[K按回车返回...")
    return
