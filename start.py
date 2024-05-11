import subprocess
from typing import Tuple
import core
import os
import play
import argparse
import subprocess
from tqdm import tqdm
from multiprocessing import Pool

def 获取控制台大小() -> Tuple[int, int]:
    columns, lines = os.get_terminal_size()
    return (columns, lines)

def start(控制台大小:Tuple[int,int]):
    线程池 = Pool(8)
    AsciIt对象 = core.AsciIt(控制台大小=控制台大小)

    for root, dirs, files in os.walk(f'{保存位置}/origin'):
        for file in files:
            if file.endswith('.jpg'):
                AsciIt对象.添加入队列(os.path.join(root, file), os.path.join(f'{保存位置}/ascii', file).replace('.jpg', '.txt'))

    list(tqdm(线程池.imap(AsciIt对象.处理, AsciIt对象.队列), total=len(AsciIt对象.队列), desc='进度'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字符化视频')
    parser.add_argument('视频路径', type=str, help='视频路径')
    parser.add_argument('保存位置', type=str, default='./cache', help='保存位置')
    parser.add_argument('帧率', type=int, default=20, help='帧率')
    args = parser.parse_args()
    音频路径='sound.mp3'
    保存位置=args.保存位置
    控制台大小=获取控制台大小()
    控制台宽度, 控制台高度 = 控制台大小
    if not os.path.exists(保存位置):
        os.mkdir(保存位置)
    with open(f'{保存位置}/info.txt','w') as f:
        f.write(' '.join([str(控制台宽度), str(控制台高度),str(args.帧率)]))
    print('开始提取音频')
    if not os.path.exists(f'{保存位置}/{音频路径}'):
        subprocess.call(f'ffmpeg -threads 4 -i {args.视频路径} -vn {保存位置}/{音频路径} -hide_banner', shell=True)
    print('音频提取完毕')
    print('开始提取帧')
    if not os.path.exists(f'{保存位置}/origin/'):
        os.mkdir(f'{保存位置}/origin/')
        subprocess.call(f'ffmpeg -threads 4 -i {args.视频路径} -r {args.帧率} {保存位置}/origin/%d.jpg -hide_banner', shell=True)
    print('所有帧已提取完毕')
    print('开始生成')
    if not os.path.exists(f'{保存位置}/ascii/'):
        os.mkdir(f'{保存位置}/ascii/')
        start(控制台大小)
    print('生成完毕')
    input('按任意键开始播放')
    play.play(args.帧率,保存位置)