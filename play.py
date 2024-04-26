import os
import sys
import time
import playsound


def play(帧率:int,缓存路径:str,音频路径:str):
    
    帧数=0

    for root, dirs, files in os.walk(f'{缓存路径}/ascii'):
        for file in files:
            if file.endswith('.txt'):
                帧数+=1

    时间间隔 = 1 / 帧率
    os.system('cls')
    sys.stdout.write('\033[25l')
    开始时间 = time.time()

    playsound.playsound(f'{缓存路径}/{音频路径}',False)
    for file in range(帧数):
        当前时间=time.time()
        预期时间=开始时间+时间间隔*file
        if 预期时间<当前时间:
            continue
        if 预期时间>当前时间:
            time.sleep(预期时间-当前时间)
        with open(os.path.join(f'{缓存路径}/ascii', str(file+1)+'.txt'), 'r', encoding='utf8') as f:
            sys.stdout.write(f.read().strip('\n'))
        sys.stdout.write('\033[H')

    os.system('cls')