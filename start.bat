pipenv run delete.py
ffmpeg -i raw.mp4 -vn -c:a copy audio.mp4
ffmpeg -i raw.mp4 -r 10 raw/%%d.jpg -hide_banner
pipenv run main.py
ffmpeg -i new/%%d.jpg -i audio.mp4 -r 10 new.mp4 -hide_banner