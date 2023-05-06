"""修改了进度条"""
from os import get_terminal_size

from progress.bar import Bar
from progress.colors import color

from modules.utils.length import get_more_length, len_abs


class CompactBar(Bar):
    def print_onto_bar(self, message: str):
        """在进度条的上方打印消息，进度条保持在下方"""
        # 光标移动到行首，并通过打印空格清空残留的进度条 ↓
        print(f"\x1b[{get_terminal_size().columns}D{(get_terminal_size().columns - 1) * ' '}"
              # 光标移动到该行的首部(\x1b[nD, n为前移个数)，将需要的信息打印出来，再将光标移动到下一行 ↓
              f"\x1b[{get_terminal_size().columns}D" + message)
        self.update()  # 更新进度条

    def writeln(self, line, shorten=False):
        """覆写writeln配合修改过后的update"""
        if self.file and self.is_tty():
            width = len_abs(line)
            if shorten:
                self._max_width = shorten
            elif width < self._max_width:
                # Add padding to cover previous contents
                line += ' ' * (self._max_width - width)
            else:
                self._max_width = width
            print('\r' + line, end='', file=self.file)
            self.file.flush()

    def update(self):
        """
        覆写原有的update方法，自适应终端宽度
        支持中文
        """
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length

        message = self.message % self
        bar = color(self.fill * filled_length, fg=self.color)
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
                        suffix])
        # 以上为原本update代码
        term_size = get_terminal_size().columns
        shorten = False
        if len_abs(line) > term_size:  # 检测完整长度是否小于终端长度
            if len_abs(line) - len_abs(''.join([bar, empty])) <= term_size:  # 检测无进度条时是否小于终端长度
                width = term_size - (len_abs(line) - len_abs("".join([bar, empty]))) - 1
                filled_length = int(width * self.progress)
                empty_length = width - filled_length
                bar = color(self.fill * filled_length, fg=self.color)
                empty = self.empty_fill * empty_length
                line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
                                suffix])
                shorten = len_abs(line)
            elif len_abs(''.join([message, suffix])) <= term_size:  # 检测仅有前缀后缀时是否小于终端长度
                line = ''.join([message, suffix])
                shorten = len_abs(line)
            else:  # 全部不符合时，以仅有前缀后缀的模式，直接截断
                display_length = term_size-get_more_length(''.join([message, suffix])[:term_size])-3
                if display_length < 0:
                    display_length = 0
                line = ''.join([message, suffix])[:display_length]+"..."
                shorten = len_abs(line)
        self.writeln(line, shorten=shorten)


class CompactArrowBar(CompactBar):
    def update(self):
        """
                覆写原有的update方法，自适应终端宽度
                支持中文
                """
        filled_length = int(self.width * self.progress)
        empty_length = self.width - filled_length

        message = self.message % self
        s = "=" * filled_length
        if s:
            s = s[:-1] + ">"
        bar = color(s, fg=self.color)
        empty = self.empty_fill * empty_length
        suffix = self.suffix % self
        line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
                        suffix])
        # 以上为原本update代码
        term_size = get_terminal_size().columns
        shorten = False
        if len_abs(line) > term_size:  # 检测完整长度是否小于终端长度
            if len_abs(line) - len_abs(''.join([bar, empty])) <= term_size:  # 检测无进度条时是否小于终端长度
                width = term_size - (len_abs(line) - len_abs("".join([bar, empty]))) - 1
                filled_length = int(width * self.progress)
                empty_length = width - filled_length
                s = "=" * filled_length
                if s:
                    s = s[:-1] + ">"
                bar = color(s, fg=self.color)
                empty = self.empty_fill * empty_length
                line = ''.join([message, self.bar_prefix, bar, empty, self.bar_suffix,
                                suffix])
                shorten = len_abs(line)
            elif len_abs(''.join([message, suffix])) <= term_size:  # 检测仅有前缀后缀时是否小于终端长度
                line = ''.join([message, suffix])
                shorten = len_abs(line)
            else:  # 全部不符合时，以仅有前缀后缀的模式，直接截断
                display_length = term_size - get_more_length(''.join([message, suffix])[:term_size]) - 3
                if display_length < 0:
                    display_length = 0
                line = ''.join([message, suffix])[:display_length] + "..."
                shorten = len_abs(line)
        self.writeln(line, shorten=shorten)


def bprint(content, bar: CompactBar = None):
    """添加对进度条的支持的print, 若传入bar参数, 则使用print_onto_bar参数来打印内容"""
    if bar:
        bar.print_onto_bar(content)
    else:
        print(content)
