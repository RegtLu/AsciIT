import subprocess
from typing import Tuple
import delete
import core
import os
import play
import argparse
import subprocess
import shutil

def 获取控制台大小() -> Tuple[int, int]:
    columns, lines = shutil.get_terminal_size()
    return (columns, lines)

def start(控制台大小:Tuple[int,int]):
    线程池 = core.Pool(8)
    AsciIt对象 = core.AsciIt(控制台大小=控制台大小)

    for root, dirs, files in os.walk('./cache/raw'):
        for file in files:
            if file.endswith('.jpg'):
                AsciIt对象.添加入队列(os.path.join(root, file), os.path.join('./cache/new', file).replace('.jpg', '.txt'))

    list(core.tqdm(线程池.imap(AsciIt对象.处理, AsciIt对象.队列), total=len(AsciIt对象.队列), desc='进度'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字符化视频')
    parser.add_argument('video_path', type=str, help='视频路径')
    parser.add_argument('frame_rate', type=float, default=20, help='帧率')
    args = parser.parse_args()
    input('缩小控制台(Ctrl+滚轮),按任意键确定控制台大小\n确定后可以重新放大')
    控制台大小=获取控制台大小()
    print(f'控制台大小为: {控制台大小}')
    delete.delete()
    print('缓存清理完毕')
    print('开始提取音频')
    subprocess.call(f"ffmpeg -y -i {args.video_path} -vn ./cache/audio.mp3 -hide_banner")
    print('音频提取完毕')
    print('开始提取帧')
    subprocess.call(f"ffmpeg -i {args.video_path} -r {args.frame_rate} ./cache/raw/%d.jpg -hide_banner")
    print('所有帧已提取完毕')
    print('开始生成')
    start(控制台大小)
    print('生成完毕')
    input('缩小控制台(Ctrl+滚轮),按任意键开始播放\n如有变形,请将控制台字体大小修改为长宽相同')
    play.play(args.frame_rate)