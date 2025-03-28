import yt_dlp
from pathlib import Path
import shutil
from moviepy.editor import *
from datetime import datetime
import os


DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "/"
CURR_DIR = str(Path().resolve()) + "/"
SOURCE_VIDEO_CACHE = f"{CURR_DIR}/source_video_cache"
OUTPUT_VIDEO_CACHE = f"{CURR_DIR}/output_video_cache"
current_datetime_as_str = datetime.now().strftime('%Y.%m.%d_%H%M%S')
result_filename = f"{current_datetime_as_str}_result.mp4"
result_file_path = f"{OUTPUT_VIDEO_CACHE}/{result_filename}"
desktop_file_path = f"{DESKTOP}/{result_filename}"


def get_folder_size(folder_path):
    return sum(f.stat().st_size for f in Path(folder_path).rglob('*') if f.is_file())


def clear_folder(folder_path):
    print(f"Clearing {folder_path}")
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"File {file_name} deleted.")


def clear_caches():
    clear_folder(OUTPUT_VIDEO_CACHE)

    source_cache_total_size = get_folder_size(SOURCE_VIDEO_CACHE)
    if source_cache_total_size > 5 * 1024 * 1024 * 1024:
        clear_folder(SOURCE_VIDEO_CACHE)
    else:
        print("Source video cache size is less than 5 Gb. No need to clear")


def download_video_from_youtube(url, source_video_filename):
    # ydl_opts_format = {
    #     'listformats': True
    # }
    # with yt_dlp.YoutubeDL(ydl_opts_format) as ydl:
    #     ydl.extract_info(url, download=False)

    ydl_opts = {
        'outtmpl': f'{source_video_filename}',
        'format': 'best[height<=360]'
    }
    if 'shorts' in url:
        ydl_opts['format'] = 'best[width<=360]'

    for i in range(1, 3):
        try:
            print(f"Attempt #{i} with {ydl_opts}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Start downloading video from youtube")
                ydl.download([url])
                print("Finished downloading")
                break
        except:
            print(f"Attempt failed")
            ydl_opts.pop("format")
            continue


def cut_video(filename, start_time, end_time):
    start_min = int(start_time.split(":")[0])
    start_sec = int(start_time.split(":")[1])
    end_min = int(end_time.split(":")[0])
    end_sec = int(end_time.split(":")[1])
    print("Start cutting a fragment")
    clip = VideoFileClip(filename)
    clip1 = clip.subclip((start_min, start_sec), (end_min, end_sec))
    clip1.write_videofile(result_file_path, codec='libx264')
    clip.close()
    clip1.close()
    print("Finish cutting")


def calculate_video_hash(url):
    if "youtu.be" in url:
        video_hash = url.split("?")[0].split("/")[-1]
    elif "shorts" in url:
        video_hash = url.split("/")[-1]
    else:
        video_hash = url.split("&")[0].split("=")[1]

    print(f"URL {url}, video hash {video_hash}")
    return video_hash


def copy_to_desktop(video_file_path):
    print("Copy file to desktop")
    shutil.copy(video_file_path, desktop_file_path)


def download_video(url):
    video_hash = calculate_video_hash(url)
    source_video_filepath = f"{SOURCE_VIDEO_CACHE}/{video_hash}.mp4"
    if not os.path.isfile(source_video_filepath):
        download_video_from_youtube(url, source_video_filepath)

    copy_to_desktop(source_video_filepath)

    return source_video_filepath


def download_and_cut(args):
    if len(args) != 3:
        raise ValueError("Should be exact 3 args - url, start time, end time")

    url, start_time, end_time = args[0], args[1], args[2]
    source_video_filepath = download_video(url)
    cut_video(source_video_filepath, start_time, end_time)

    copy_to_desktop(result_file_path)
    return result_file_path


# download_and_cut(['https://www.youtube.com/watch?v=cpp69ghR1IM', '0:42', '1:03'])
clear_caches()
