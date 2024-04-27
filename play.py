import os
import sys
import time
import playsound

def 内容提供(缓存路径:str):
    结束=False
    索引=0
    while not 结束:
        索引+=1
        try:
            yield open(os.path.join(f'{缓存路径}/ascii', str(索引+1)+'.txt'), 'r', encoding='utf8').read().strip('\n')
        except:
            结束=True
    yield False
    return

def play(帧率:int,缓存路径:str,音频路径:str):
    时间间隔 = 1 / 帧率
    当前帧=0
    os.system('cls')
    sys.stdout.write('\033[25l')
    开始时间 = time.time()
    内容提供器=内容提供(缓存路径)
    playsound.playsound(f'{缓存路径}/{音频路径}',False)
    while True:
        当前帧+=1
        当前时间=time.time()
        预期时间=开始时间+时间间隔*当前帧
        内容=next(内容提供器)
        if 预期时间<当前时间:
            continue
        if 预期时间>当前时间:
            time.sleep(预期时间-当前时间)
        if not 内容:
            break
        sys.stdout.write(内容)
        sys.stdout.write('\033[H')
    os.system('cls')