"""一些有关调整进度条的设置"""
from os import get_terminal_size

from progress.bar import Bar


def suit_length(bar: Bar, original: Bar):
    """尽量调整进度条大小去匹配终端宽度"""
    length = get_terminal_size().columns
    original_length = original.width + len((original.message +
                                            original.bar_suffix +
                                            original.bar_prefix +
                                            original.suffix) % bar)
    if length >= original_length:
        return
    if length < len(str(bar.max) + "/" + str(bar.index)):
        bar.bar_suffix = bar.suffix = bar.bar_prefix = ""
        bar.width = 0
        bar.suffix = Bar.suffix
    elif length >= original_length - bar.width:
        bar.width = length - len((bar.message + bar.bar_suffix + bar.bar_prefix + bar.suffix) % bar)
    elif length >= original_length - (bar.width + len(bar.suffix % bar)) and "(index)" in bar.message:
        bar.suffix = ""
        bar.width = length - len((bar.message + bar.bar_suffix + bar.bar_prefix + bar.suffix) % bar)
    elif length >= original_length - (bar.width + len(bar.message % bar)) and "(index)" in bar.suffix:
        bar.message = ""
        bar.width = length - len((bar.message + bar.bar_suffix + bar.bar_prefix + bar.suffix) % bar)
    elif length >= original_length - (bar.width + len((bar.message + bar.suffix) % bar)) + Bar.suffix % bar:
        bar.message = ""
        bar.suffix = Bar.suffix
        bar.width = length - len((bar.message + bar.bar_suffix + bar.bar_prefix + bar.suffix) % bar)
    bar.update()
    return
