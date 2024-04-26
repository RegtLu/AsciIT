import argparse
import os
import sys
import time
import playsound


def play(帧率):
    
    playlist = []

    for root, dirs, files in os.walk('./cache/new'):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf8') as f:
                    content = f.read().strip('\n')
                playlist.append((int(file.strip('.txt')), content))

    playlist = sorted(playlist, key=lambda x: x[0])

    rate = 帧率
    delta_time = 1 / rate
    os.system('cls')
    sys.stdout.write('\033[25l')
    start_time = time.time()

    playsound.playsound('./cache/audio.mp3',False)
    for file, content in playlist:
        sys.stdout.write(content)

        current_time = time.time()
        elapsed_time = current_time - start_time
        expected_next_time = delta_time * file

        if elapsed_time < expected_next_time:
            time.sleep(expected_next_time - elapsed_time)

        sys.stdout.write('\033[H')

    end_time = time.time()
    os.system('cls')
    print(f'总时长: {end_time - start_time}s')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='字符化播放器')
    parser.add_argument('frame_rate', type=float, default=30, help='帧率')
    args = parser.parse_args()
    play(args.frame_rate)