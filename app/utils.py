import os
import shutil
import subprocess


def run(command):
    output = subprocess.run(command, cwd=os.getcwd(), stdout=subprocess.PIPE)
    return output.stdout.decode('UTF-8')


def to_gib(number):
    return number // (2 ** 30)


def free_space_at(path):
    if os.path.exists(path):
        total, used, free = shutil.disk_usage(path)
        return to_gib(free)
