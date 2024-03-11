from pytube import YouTube
from pathlib import Path
from moviepy.editor import *
import argparse
from datetime import datetime
import os

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "/"
CURR_DIR = str(Path().resolve()) + "/"
temp_file = "temp.mp4"
temp_file_path = CURR_DIR + "temp.mp4"
current_datetime_as_str = datetime.now().strftime('%Y.%m.%d_%H%M%S')
result_file = "{}_result.mp4".format(current_datetime_as_str)
result_file_path = result_file

parser = argparse.ArgumentParser()
parser.add_argument('-url')
parser.add_argument('-start')
parser.add_argument('-end')


def download_video_from_youtube(url):
    video = YouTube(url)
    print("Start downloading video from youtube")
    streams = video.streams \
        .filter(progressive=True, file_extension="mp4") \
        .filter(res="360p") \
        .first() \
        .download(output_path=CURR_DIR, filename=temp_file)

    print("Finished downloading")


def cut_vide_and_move_to_desktop(start_time, end_time):
    start_min = int(start_time.split(":")[0])
    start_sec = int(start_time.split(":")[1])
    end_min = int(end_time.split(":")[0])
    end_sec = int(end_time.split(":")[1])
    print("Start cutting a fragment")
    clip = VideoFileClip(temp_file)
    clip1 = clip.subclip((start_min, start_sec), (end_min, end_sec))
    clip1.write_videofile(result_file, codec='libx264')
    clip.close()
    clip1.close()
    print("Finish cutting")

    print("Move file to desktop")
    Path(result_file_path).rename(desktop + result_file)

    print()


def main():
    # args = parser.parse_args()
    # url, start_time, end_time = args.url, args.start, args.end
    url, start_time, end_time = "url", "1:02", "1:52"
    if not os.path.isfile(temp_file_path):
        download_video_from_youtube(url)
    cut_vide_and_move_to_desktop(start_time, end_time)


main()
