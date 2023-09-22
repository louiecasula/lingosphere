import sys, subprocess, re


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def clear_screen():
    operating_system = sys.platform

    if operating_system == "win32":
        subprocess.run("cls", shell=True)
    elif operating_system == "linux" or operating_system == "darwin":
        subprocess.run("clear", shell=True)


def highlight(word, string):
    replacement = color.BOLD + color.PURPLE + word.lower() + color.END
    compiled = re.compile(re.escape(word), re.IGNORECASE)
    print(compiled.sub(replacement, string))
