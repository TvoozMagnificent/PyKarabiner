
from json import dumps as string
from random import randint as random

def r(): return str(random(0, 10**10-1)).zfill(10)

with open('config.txt') as config: prefix = config.read().strip()
def write(content):
    with open(f'{prefix}/{r()}.json', 'a+') as file: file.write(content)

def import_modification(modification): write(string(modification.to_json()))
