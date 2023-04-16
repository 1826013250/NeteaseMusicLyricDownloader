"""一些有关计算长度的工具"""


def len_abs(content):
    """针对中文：将一个汉字识别为2个长度，而不是1个"""

    return len(content) + (len(content.encode("utf-8")) - len(content)) // 2
