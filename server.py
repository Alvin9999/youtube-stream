# -*- coding: utf-8 -*-
# author: gfw-breaker

import pafy
import requests
from flask import Flask
from flask import Response
from flask import stream_with_context
from flask import render_template
from flask import request

app = Flask(__name__)

video_db = {}
buffer_size = 1024 * 1024  # 1MB
youtube_url = "https://www.youtube.com/watch?v="


class VideoInfo:

    def __init__(self, id, title, url, width, height):
        self.id = id
        self.title = title
        self.url = url
        self.width = width
        self.height = height


def get_video_info(video_id):
    if not video_db.has_key(video_id):
        video = pafy.new(youtube_url + video_id)
        best = video.getbest(preftype="mp4")
        width = best.resolution.split('x')[0]
        height = best.resolution.split('x')[1]
        video_info = VideoInfo(video_id, video.title, best.url, width, height)
        video_db[video_id] = video_info
        return video_info
    else:
        return video_db[video_id]


def get_stream(action, video_id):
    video_info = get_video_info(video_id)
    req = requests.get(video_info.url, stream=True, verify=False)
    file_name = 'filename=' + video_info.title.encode('utf-8') + '.mp4'
    if action == 'download':
        file_name = 'attachment; ' + file_name
    headers = {
        'Content-Type': 'video/mp4',
        'Content-Disposition': file_name
    }


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/watch')
def watch():
    video_id = request.args.get('v')
    video_info = get_video_info(video_id)
    return render_template("watch.html", id=video_info.id, title=video_info.title,
                           width=video_info.width, height=video_info.height)


@app.route('/live')
def play():
    video_id = request.args.get('v')
    return get_stream('live', video_id)


@app.route('/download')
def download():
    video_id = request.args.get('v')
    return get_stream('download', video_id)


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()  # suppress SSL warning
    app.run(host='local_server_ip', port=9999, threaded=True)

## video_id: ZUYl1dNtzCk
