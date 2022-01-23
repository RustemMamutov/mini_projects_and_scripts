from pytube import YouTube
from pydub import AudioSegment
import subprocess
import pathlib
import os
import re
import math

URL = "https://www.youtube.com/watch?v=RR0WvtX4o3o"
RESULT_FILE_NAME = "кац_ссср"
VOLUME_DELTA_DB = 12

directory_path = str(pathlib.Path().resolve()).replace("\\", "/")
# AudioSegment.ffmpeg = directory_path + "/ffmpeg"
AudioSegment.converter = directory_path + r"/ffmpeg.exe"
AudioSegment.ffmpeg = directory_path + r"/ffmpeg.exe"
AudioSegment.ffprobe = directory_path + r"/ffprobe.exe"


def get_rate_as_int(stream_):
    return int(stream_.abr.replace('kbps', ''))


def download_timecodes(youtube_object_):
    if "0:00" in youtube_object_.description:
        result = re.findall("\n\d:\d\d", youtube_object_.description) + \
                 re.findall("\n\d\d:\d\d", youtube_object_.description)
        return [x.replace("\n", "") for x in result]

    return None


def download_audio(youtube_object_, result_filename_):
    print("START downloading audio from: " + youtube_object_.title)

    audio_streams = youtube_object_.streams.filter(only_audio=True)
    target_stream = audio_streams[0]
    for stream in audio_streams:
        target_stream = stream if get_rate_as_int(stream) > get_rate_as_int(target_stream) else target_stream

    _result_file = target_stream.download(filename=result_filename_ + ".mp3")
    print('Task Completed! Result file: ' + _result_file)
    return _result_file


def convert_audio_before_split(file_full_path_):
    converted_file_full_path = "{}/{}_converted.mp3".format(directory_path, RESULT_FILE_NAME)
    subprocess.run("ffmpeg -i {} -vn {}".format(file_full_path_, converted_file_full_path))
    os.remove(file_full_path_)
    os.rename(converted_file_full_path, file_full_path_)


def split_audio_by_timecodes(file_full_path_, time_codes_):
    song = AudioSegment.from_mp3(file_full_path_) + VOLUME_DELTA_DB

    for i in range(0, len(time_codes_)):
        time_now = time_codes_[i]
        time_next = "1000:00" if i == (len(time_codes_) - 1) else time_codes_[i + 1]
        delta = 0 if i == 0 else -2000

        start_min = int(time_now.split(":")[0])
        start_sec = int(time_now.split(":")[1])

        end_min = int(time_next.split(":")[0])
        end_sec = int(time_next.split(":")[1])
        start_time = start_min * 60 * 1000 + start_sec * 1000 + delta
        end_time = end_min * 60 * 1000 + end_sec * 1000

        extract = song[start_time:end_time]
        # Saving
        # extract.export('{}_{}.mp3'.format(RESULT_FILE_NAME, '{:02d}'.format(i + 1)), format="mp3")
        filename = '{}_{}-{}.mp3'.format(RESULT_FILE_NAME, '{:02d}'.format(start_min),
                                         '{:02d}'.format(start_sec))
        extract.export(filename, format="mp3")


def split_audio_by_parts(file_full_path_, part_length_sec_):
    song = AudioSegment.from_mp3(file_full_path_) + VOLUME_DELTA_DB
    max_index = math.ceil(song.duration_seconds / part_length_sec_)
    for i in range(0, max_index):
        delta = 0 if i == 0 else -2000

        start_time = i * part_length_sec_ * 1000 + delta
        end_time = (i + 1) * part_length_sec_ * 1000

        extract = song[start_time:end_time]
        # Saving
        extract.export('{}_{}.mp3'.format(RESULT_FILE_NAME, '{:02d}'.format(i + 1)), format="mp3")


def main():
    audio_file_full_path = "{}/{}.mp3".format(directory_path, RESULT_FILE_NAME)
    youtube = YouTube(URL)
    download_audio(youtube, RESULT_FILE_NAME)
    # time_codes = download_timecodes(youtube)
    convert_audio_before_split(audio_file_full_path)
    # split_audio_by_timecodes(audio_file_full_path, time_codes)

    split_audio_by_parts(audio_file_full_path, 1200)


main()
