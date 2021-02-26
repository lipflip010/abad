import os
import subprocess


def run(command):
    output = subprocess.run(command, cwd=os.getcwd(), stdout=subprocess.PIPE)
    return output.stdout.decode('UTF-8')


def to_gib(number):
    return number // (2 ** 30)
