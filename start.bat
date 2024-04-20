pipenv run delete.py
ffmpeg -i raw.mp4 -vn audio.mp3 -hide_banner
ffmpeg -i raw.mp4 -r 20 raw/%%d.jpg -hide_banner
pipenv run main.py
pipenv run play.py