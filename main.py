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
