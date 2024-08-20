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

        # Função para cortar o vídeo
        cut_video_filename = f"{video_id}_cut.mp4" # Define o nome do arquivo cortado, ID+cut.mp4
        cut_video_path = os.path.join(VIDEO_DIR, cut_video_filename) # Caminho onde o vídeo será salvo

        # Usando o ffmpeg para realizar os cortes

        ffmpeg_command = [
            'ffmpeg', '-i', video_path, '-ss', start_time, '-to', end_time,
            '-c', 'copy', cut_video_path
        ]
        # - i é o caminho do vídeo original | -ss, start time, define o tempo de início | -to, end time, tempo de término | -c, copy, copia o fluxo de dados diretamente

        subprocess.run(ffmpeg_command)

        # Retorna o arquivo diretamente para download
        return send_file(cut_video_path, as_attachment=True)

# App para deletar o arquivo de vídeo original após download

@app.route('/delete', methods=['POST'])
def delete():
    video_id = request.form['video_id']

    for file in os.listdir(VIDEO_DIR):
        if video_id in file:
            os.remove(os.path.join(VIDEO_DIR, file))

    return redirect(url_for('index'))

# Rodando e Debugando
if __name__ == '__main__':
    app.run(debug=True)