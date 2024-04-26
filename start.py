import subprocess
from typing import Tuple
import core
import os
import play
import argparse
import subprocess
import shutil
from tqdm import tqdm
from multiprocessing import Pool

def 获取控制台大小() -> Tuple[int, int]:
    columns, lines = shutil.get_terminal_size()
    return (columns, lines)

def start(控制台大小:Tuple[int,int]):
    线程池 = Pool(8)
    AsciIt对象 = core.AsciIt(控制台大小=控制台大小)

    for root, dirs, files in os.walk(f'{缓存路径}/origin'):
        for file in files:
            if file.endswith('.jpg'):
                AsciIt对象.添加入队列(os.path.join(root, file), os.path.join(f'{缓存路径}/ascii', file).replace('.jpg', '.txt'))

    list(tqdm(线程池.imap(AsciIt对象.处理, AsciIt对象.队列), total=len(AsciIt对象.队列), desc='进度'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字符化视频')
    parser.add_argument('video_path', type=str, help='视频路径')
    parser.add_argument('frame_rate', type=float, default=30, help='帧率')
    args = parser.parse_args()
    音频路径=args.video_path.replace('.mp4','.mp3')
    缓存路径=args.video_path.replace('.mp4','')
    控制台大小=获取控制台大小()
    控制台宽度, 控制台高度 = 控制台大小
    ''''''
    if not os.path.exists(缓存路径):
        os.mkdir(缓存路径)
    print('开始提取音频')
    if not os.path.exists(f'{缓存路径}/{音频路径}'):
        subprocess.call(f"ffmpeg -y -i {args.video_path} -vn {缓存路径}/{音频路径} -hide_banner")
    print('音频提取完毕')
    print('开始提取帧')
    if not os.path.exists(f'{缓存路径}/origin/'):
        os.mkdir(f'{缓存路径}/origin/')
        #subprocess.call(f'ffmpeg -i {args.video_path} -r {args.frame_rate} -vf "scale={控制台宽度}:{控制台高度}:force_original_aspect_ratio=decrease:flags=lanczos" {缓存路径}/origin/%d.jpg -hide_banner')
        subprocess.call(f'ffmpeg -i {args.video_path} -r {args.frame_rate} {缓存路径}/origin/%d.jpg -hide_banner')
    print('所有帧已提取完毕')
    print('开始生成')
    if not os.path.exists(f'{缓存路径}/ascii/'):
        os.mkdir(f'{缓存路径}/ascii/')
        start(控制台大小)
    print('生成完毕')
    input('按任意键开始播放')
    play.play(args.frame_rate,缓存路径,音频路径)