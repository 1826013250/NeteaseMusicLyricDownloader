import binascii
import json
import os
import struct
from base64 import b64decode
from multiprocessing import Process, Queue
from queue import Empty

from progress.bar import Bar
from Cryptodome.Cipher import AES
from mutagen import File, flac
from mutagen.id3 import ID3, TPE1, APIC, COMM, TIT2, TALB

from modules.clear_screen import clear
from modules.get_song import get_song_lyric
from modules.inputs import cinput, rinput


def load_information_from_song(path):
    """从音乐文件中的 Comment 字段获取 163 key 并解密返回歌曲信息"""
    file = File(path)  # 使用 mutagen 获取歌曲信息
    if os.path.splitext(path)[-1] == ".mp3":  # 当文件为 mp3 时使用 ID3 格式读取
        if file.tags.get("COMM::XXX"):
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

    def unpad(s):  # 创建清理针对于网易云的 AES-128-ECB 解密后末尾占位符的函数
        if type(s[-1]) == int:
            end = s[-1]
        else:
            end = ord(s[-1])
        return s[0:-end]
        # return s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]  更加清晰的理解 ↑

    cryptor = AES.new(b"#14ljk_!\\]&0U<'(", AES.MODE_ECB)  # 使用密钥创建解密器

    # 下方这一行将密文 ciphertext 转换为 bytes 后进行 base64 解码, 得到加密过的 AES 密文
    # 再通过上方创建的 AES 128-ECB 的解密器进行解密, 然后使用 unpad 清除末尾无用的占位符后得到结果
    try:
        r = unpad((cryptor.decrypt(b64decode(bytes(ciphertext, "utf-8"))).decode("utf-8")))
    except ValueError:
        return "decrypt_failed"

    if r:
        if r[:5] == "music":
            return json.loads(r[6:])
        else:
            return "not_a_normal_music"
    else:
        return "decrypt_failed"


def load_and_decrypt_from_ncm(file_path, targetdir):  # nondanee的源代码, 根据需求更改了某些东西
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s: s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]
    f = open(file_path, 'rb')
    header = f.read(8)
    assert binascii.b2a_hex(header) == b'4354454e4644414d'
    f.seek(2, 1)
    key_length = f.read(4)
    key_length = struct.unpack('<I', bytes(key_length))[0]
    key_data = f.read(key_length)
    key_data_array = bytearray(key_data)
    for i in range(0, len(key_data_array)):
        key_data_array[i] ^= 0x64
    key_data = bytes(key_data_array)
    cryptor = AES.new(core_key, AES.MODE_ECB)
    key_data = unpad(cryptor.decrypt(key_data))[17:]
    key_length = len(key_data)
    key_data = bytearray(key_data)
    key_box = bytearray(range(256))
    c = 0
    last_byte = 0
    key_offset = 0
    for i in range(256):
        swap = key_box[i]
        c = (swap + last_byte + key_data[key_offset]) & 0xff
        key_offset += 1
        if key_offset >= key_length:
            key_offset = 0
        key_box[i] = key_box[c]
        key_box[c] = swap
        last_byte = c
    meta_length = f.read(4)
    meta_length = struct.unpack('<I', bytes(meta_length))[0]
    meta_data = f.read(meta_length)
    meta_data_array = bytearray(meta_data)
    for i in range(0, len(meta_data_array)):
        meta_data_array[i] ^= 0x63
    meta_data = bytes(meta_data_array)
    comment = meta_data
    meta_data = b64decode(meta_data[22:])
    cryptor = AES.new(meta_key, AES.MODE_ECB)
    meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')[6:]
    meta_data = json.loads(meta_data)
    crc32 = f.read(4)
    crc32 = struct.unpack('<I', bytes(crc32))[0]
    f.seek(5, 1)
    image_size = f.read(4)
    image_size = struct.unpack('<I', bytes(image_size))[0]
    image_data = f.read(image_size)
    file_name = f.name.split("/")[-1].split(".ncm")[0] + '.' + meta_data['format']
    m = open(os.path.join(targetdir, file_name), 'wb')
    chunk = bytearray()
    while True:
        chunk = bytearray(f.read(0x8000))
        chunk_length = len(chunk)
        if not chunk:
            break
        for i in range(1, chunk_length + 1):
            j = i & 0xff
            chunk[i - 1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
        m.write(chunk)
    m.close()
    f.close()

    # 对解密后的文件进行信息补全
    if meta_data["format"] == "mp3":  # 针对 mp3 使用 ID3 进行信息补全
        audio = ID3(os.path.join(targetdir, os.path.splitext(file_path.split("/")[-1])[0] + ".mp3"))
        artists = []
        for i in meta_data["artist"]:
            artists.append(i[0])
        audio["TPE1"] = TPE1(encoding=3, text=artists)  # 插入歌手
        audio["APIC"] = APIC(encoding=3, mime='image/jpg', type=3, desc='', data=image_data)  # 插入封面
        audio["COMM::XXX"] = COMM(encoding=3, lang='XXX', desc='', text=[comment.decode("utf-8")])  # 插入 163 key 注释
        audio["TIT2"] = TIT2(encoding=3, text=[meta_data["musicName"]])  # 插入歌曲名
        audio["TALB"] = TALB(encoding=3, text=[meta_data["album"]])  # 插入专辑名
        audio.save()
    elif meta_data["format"] == "flac":  # 针对 flac 使用 FLAC 进行信息补全
        audio = flac.FLAC(os.path.join(targetdir, os.path.splitext(file_path.split("/")[-1])[0] + ".flac"))
        artists = []
        for i in meta_data["artist"]:
            artists.append(i[0])
        audio["artist"] = artists[:]  # 插入歌手
        audio["title"] = [meta_data["musicName"]]  # 插入歌曲名
        audio["album"] = [meta_data["album"]]  # 插入专辑名
        audio["description"] = comment.decode("utf-8")  # 插入 163 key 注释
        audio.save()

    return meta_data


def process_work(path, filename, target, q_err: Queue, q_info: Queue):
    try:
        result = load_and_decrypt_from_ncm(path, target)
    except AssertionError:
        q_err.put(f"\t- 文件 \"{filename}\" 破解失败!")
    else:
        q_info.put(result)


def get_lyric_from_folder(lyric_path: str):
    clear()
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
            else:
                musics.append({"id": result['musicId'], "name": result["musicName"], "artists": result["artist"]})
        elif ext == ".ncm":  # 对于 ncm 先加入到列表，等待解密
            ncm_files.append(i)
        else:
            pass

    if ncm_files:
        while True:
            print(f"\n发现{len(ncm_files)}个ncm加密文件!")
            print("请问解密后的文件保存在哪里?\n"
                  "[1] 保存在相同文件夹内\n[2] 保存在程序设定的下载文件夹中\n[3] 保存在自定义文件夹内\n[q] 取消解密,下载歌词时将忽略这些文件")
            select = rinput("请选择: ")
            if select == 'q':
                target_path = "NOT_DECRYPT"
                break
            elif select == '1':
                target_path = path
                break
            elif select == '2':
                target_path = lyric_path
                break
            elif select == '3':
                target_path = input("请输入: ").strip()
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
            with Bar("正在破解", max=len(ncm_files)) as bar:
                total = len(ncm_files)
                finished = 0  # 已经分配的人物数量
                while True:  # 进入循环，执行  新建进程->检测队列->检测任务完成  的循环
                    if current_process <= max_process and finished < total:  # 分配进程
                        Process(target=process_work,
                                args=(os.path.join(path, ncm_files[finished]),
                                      ncm_files[finished],
                                      target_path,
                                      q_err,
                                      q_info)).start()
                        finished += 1
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
                            bar.next()
                        except Empty:
                            break
                    if passed >= len(ncm_files):
                        break
            if errors:
                print("解密过程中发现了以下错误:")
                for i in errors:
                    print(i)

    # 汇报索引结果
    print(f"\n索引完毕!共找到{fails + len(musics) + len(ncm_files)}个目标文件\n{len(musics)}个文件已载入\n{fails}个文件失败")
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
            break
        else:
            try:
                input("无效选择, 若取消请按 ^C ,继续请按回车")
                clear()
            except KeyboardInterrupt:
                return

    clear()
    for i in range(0, len(musics)):  # 根据索引结果获取歌词
        print("\n进度: %d/%d" % (i + 1, len(musics)))
        if get_song_lyric(musics[i], lyric_path, allinfo=True) == "dl_err_connection":
            input("下载发生错误！可能是连接被拒绝!请检查网络后再试\n按回车键继续任务(该任务会被跳过)...")
    if ncm_files:
        if target_path != "NOT_DECRYPT":
            agree = rinput("是否删除原ncm文件? (y/n)")
            if agree == "y":
                for i in range(0, len(ncm_files)):
                    print("删除进度: %d/%d\n -> %s\033[F" % (i + 1, len(ncm_files), ncm_files[i]), end="")
                    os.remove(os.path.join(path, ncm_files[i]))
            else:
                print("取消.", end="")
    input("\n\033[K按回车返回...")
    return
