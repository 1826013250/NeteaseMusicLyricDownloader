"""一些有的没有的装饰器"""


def escape_file_not_found(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return "file_not_found"
    return wrapper


def escape_decrypt_unsatisfied_file(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (AssertionError, IsADirectoryError):
            return "file_not_satisfied"
    return wrapper


def escape_permission_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError:
            return "perm_error"
    return wrapper
