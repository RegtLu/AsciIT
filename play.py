import argparse
import os
import sys
import time
import playsound


def play(帧率):
    
    帧数=0

    for root, dirs, files in os.walk('./cache/new'):
        for file in files:
            if file.endswith('.txt'):
                帧数+=1

    时间间隔 = 1 / 帧率
    os.system('cls')
    sys.stdout.write('\033[25l')
    开始时间 = time.time()

    playsound.playsound('./cache/audio.mp3',False)
    for file in range(帧数):
        当前时间=time.time()
        预期时间=开始时间+时间间隔*file
        if 预期时间<当前时间:
            continue
        if 预期时间>当前时间:
            time.sleep(预期时间-当前时间)
        with open(os.path.join('./cache/new', str(file+1)+'.txt'), 'r', encoding='utf8') as f:
            sys.stdout.write(f.read().strip('\n'))
        sys.stdout.write('\033[H')

    os.system('cls')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字符化播放器')
    parser.add_argument('frame_rate', type=float, default=30, help='帧率')
    args = parser.parse_args()
    play(args.frame_rate)