"""该模块提供几个自定义处理输入函数"""


def rinput(string: str = ''):
    """当调用该函数时，同input()一样，但是返回一个去除首位空格并全部小写的str"""
    return input(string).strip().lower()


def cinput(string: str = ''):
    """当调用该函数时，同input()一样，但是返回一个去除首尾空格的str"""
    return input(string).strip()