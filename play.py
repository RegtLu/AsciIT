import argparse
import os
import shutil
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

def play(帧率:int,缓存路径:str):
    时间间隔 = 1 / 帧率
    当前帧=0
    os.system('cls')
    sys.stdout.write('\033[25l')
    开始时间 = time.time()
    内容提供器=内容提供(缓存路径)
    playsound.playsound(f'{缓存路径}/sound.mp3',False)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='播放字符化视频')
    parser.add_argument('视频位置', type=str, default='./cache', help='视频位置')
    args = parser.parse_args()
    with open(f'{args.视频位置}/info.txt','r') as f:
        控制台宽度,控制台高度,帧率=f.read().split(' ')
    info控制台宽度,info控制台高度=shutil.get_terminal_size()
    if int(控制台宽度)!=info控制台宽度 or int(控制台高度)!=info控制台高度 :
        print(f"文件控制台大小:  {shutil.get_terminal_size()[0]}x{shutil.get_terminal_size()[1]}\n当前控制台大小:  {控制台宽度}x{控制台高度}")
        exit(1)
    play(int(帧率),args.视频位置)