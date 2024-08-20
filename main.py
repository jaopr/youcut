from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import subprocess
import youtube_dl

app = Flask(__name__)
VIDEO_DIR = './downloads/'