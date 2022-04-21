import os
from pytube import YouTube
from pathlib import Path
import sys
import shutil


def youtube_check(url):
    if 'youtube' in url or 'youtu.be' in url:
        return True
    return False

def youtube_get_docs():
    text ='''
+-------------------------+
| Youtube:                |
+------+------------------+---------------------------+---------------------------------------------------------------+
|      |--info            |                           |  returns avaliable resolutions for video downloading          |
|      |-o / -option      |  video_only / audio_only  |  by dafault downloads video and audio                         |
| url  |-p / -path        |  /full/path               |  by default locates downloads into (path to script)/downloads |
|      |-n / name         |  your_name                |  by default name generates with video title                   |
|      |-r / -resolution  |  144 / 240/ ... / 2160..  |  by default resolution is highest                             |
+------+------------------+---------------------------+---------------------------------------------------------------+
'''
    return text

def youtube_opt_func_check():
    return True

def youtube_idx_func_check():
    return False

def youtube_res_func_check():
    return True

def youtube_parser(url):
    resolutions = {
                '144p': [394, 219, 160],
                '240p': [395, 242, 134],
                '360p': [396, 243, 167, 134],
                '480p': [397, 246, 245, 244, 219, 218, 168, 135],
                '720p': [398, 247, 169, 136],
                '720p_60fps': [302, 298],
                '1080p': [399, 248, 170, 137],
                '1080p_60fps': [303, 299],
                '1440p': [400, 271, 264],
                '1440p_60fps': [308],
                '2160p': [401, 313, 272, 138],
                '2160p_60fps': [315, 302, 266,]
                }
    res_list = ['144p',
                '240p',
                '360p',
                '480p',
                '720p',
                '720p_60fps',
                '1080p',
                '1080p_60fps',
                '1440p',
                '1440p_60fps',
                '2160p',
                '2160p_60fps']
    audio_quality_tags = {'256kbps': [172, 141],
                        '160kbps': [251],
                        '128kbps': [171, 140],
                        '70kbps': [250],
                        '60kbps': [249],
                        '48kbps': [139]
                        }
    audio_qualities = ['256kbps',
                    '160kbps',
                    '128kbps',
                    '70kbps',
                    '60kbps',
                    '48kbps']
    video_res_list = []
    video_tags = {}
    audio_quality = None
    audio_quality_tag = None

    yt_streams = YouTube(url).streams

    for res in res_list:
        for itag in resolutions[res]:
            if yt_streams.get_by_itag(itag) is not None:
                video_res_list.append(res)
                video_tags[res] = itag
                break
    
    flag = 0
    for qua in audio_qualities:
        for itag in audio_quality_tags[qua]:
            if yt_streams.get_by_itag(itag) is not None:
                audio_quality = qua
                audio_quality_tag = itag
                flag = 1
                break
        if flag == 1:
            break

    return tuple(video_res_list), video_tags, audio_quality, audio_quality_tag


def youtube_info(url):
    if "youtube.com/watch?v=" in url or "youtu.be/" in url or 'youtube.com/embed/' in url:
        parsed_url = youtube_parser(url)

        text = f"  {YouTube(url).title}\n   Avaliable video resolutions: "
        for res in parsed_url[0]:
            text = f'{text + res}, '
        text = f"{text[:-2]}\n   Audio bitrate: {parsed_url[2]}"
        
        return text

    else:
        print("ERROR: Not a video link: maybe it's a channel or playlist")


def youtube_downloader(url, opts):
    if "youtube.com/watch?v=" in url or "youtu.be/" in url or 'youtube.com/embed' in url:
        if opts['index'] is not None:
            print("WARNING: -i (-index) option will be ignored, use '--help pornhub' too get more info")

        resolution = opts['resolution']
        video_only = opts['video_only']
        audio_only = opts['audio_only']
        custom_path = opts['path']
        custom_name = opts['name']

        parsed_ytpage = youtube_parser(url)
        res_list = parsed_ytpage[0]
        res_tags = parsed_ytpage[1]
        audio_tag = parsed_ytpage[3]

        if resolution == "best":
            resolution = res_list[-1]

        res_tag = res_tags[resolution]
        yt_streams = YouTube(url).streams

        prjct_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.absolute()

        try:
            os.mkdir(f'{prjct_dir}/downloads'.replace('/', os.sep))
        except:
            pass
        try:
            os.mkdir(f'{prjct_dir}/downloads/buffer'.replace('/', os.sep))
        except:
            pass

        buffer_path = f'{prjct_dir}/downloads/buffer'.replace('/', os.sep)
        video_path = f'{buffer_path}/video.mp4'.replace('/', os.sep)
        audio_path = f'{buffer_path}/audio.webm'.replace('/', os.sep)

        if custom_name is None:
            name = yt_streams.get_by_itag(res_tag).default_filename.replace(" ", "_").replace("&", "_")
        else:
            name = f'{custom_name}.mp4'
        
        if custom_path is None:
            path = f'{prjct_dir}/downloads'.replace('/', os.sep)
        else:
            path = custom_path.replace('/', os.sep)
    
        if not audio_only:
            yt_streams.get_by_itag(res_tag).download(output_path = buffer_path, filename='video.mp4')

        if audio_tag is None or video_only:

            if audio_only:
                print("ERROR: This video has no audio, it means you get nothing...")
                sys.exit()

            os.rename(video_path, f'{path}/{name}'.replace('/', os.sep))
            shutil.rmtree(buffer_path)
            return "Video download complete!"

        else:
            yt_streams.get_by_itag(audio_tag).download(output_path = buffer_path, filename='audio.webm')
            if audio_only:
                os.rename(audio_path, f'{path}/{name}'.replace('/', os.sep))
                shutil.rmtree(buffer_path)
                return "Audio download complete!"
            
            else:
                cmd = f"ffmpeg -i {audio_path} -i {video_path} -c:v copy {path}/{name}".replace('/', os.sep)
                os.system(cmd)
                shutil.rmtree(buffer_path)
                return "Video and audio download complete!"

    else:
        print("ERROR: Not a video link: maybe it's a channel or playlist")
