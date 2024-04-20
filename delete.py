from os import mkdir
import shutil

def delete():
    try:
        shutil.rmtree('./cache/')
    except:
        pass
    mkdir('cache')
    mkdir('cache/raw')
    mkdir('cache/new')