from os import mkdir
import shutil

try:
    shutil.rmtree('./new/')
    shutil.rmtree('./raw/')
except:
    pass
mkdir('new/')
mkdir('raw/')