from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import subprocess
import youtube_dl

app = Flask(__name__)
VIDEO_DIR = './downloads/'

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    # Função para baixar o vídeo
    ydl_opts = {
        'outtmpl': VIDEO_DIR + '%(id)s.%(ext)s', # - outtmpl, modelo do nome do arquivo | '%(id)s' marcador de posição, será substituido pelo ID do vídeo | '%(ext)s' será substituido pela extensão do arquivo
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info['id']
        video_ext = info['ext']
        video_filename = f"{video_id}.{video_ext}"
        video_path = os.path.join(VIDEO_DIR, video_filename)

