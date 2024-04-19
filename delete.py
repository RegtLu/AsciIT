from os import mkdir
import shutil

shutil.rmtree('./new/')
shutil.rmtree('./raw/')
mkdir('new/')
mkdir('raw/')