import os
import time
import playsound


def play(帧率):
    
    playlist = []

    for root, dirs, files in os.walk('./cache/new'):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf8') as f:
                    content = f.read()
                playlist.append((int(file.strip('.txt')), content))

    playlist = sorted(playlist, key=lambda x: x[0])

    rate = 帧率
    delta_time = 1 / rate
    print('\033[?25l')
    os.system('cls')
    start_time = time.time()

    playsound.playsound('./cache/audio.mp3',False)
    for file, content in playlist:
        print(content)

        current_time = time.time()
        elapsed_time = current_time - start_time
        expected_next_time = delta_time * (file + 1)

        if elapsed_time < expected_next_time:
            time.sleep(expected_next_time - elapsed_time)

        print('\033[H')

    print('\033[?25h')
    end_time = time.time()
    print(f'总时长: {end_time - start_time}s')