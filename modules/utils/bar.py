"""修改了进度条"""
from os import get_terminal_size

from progress.bar import Bar

from modules.utils.length import get_more_length


class CompactBar(Bar):
    def print_onto_bar(self, message: str):
        print()
        self.update()
        print(f"\x1b[1A\x1b[{get_terminal_size().columns}D{(get_terminal_size().columns-1) * ' '}"
              f"\x1b[{get_terminal_size().columns}D"+message[:(get_terminal_size().columns - get_more_length(message))])
        self.update()

    def next_without_newline(self):
        self.next()
