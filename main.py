from flask import Flask,render_template,send_file,request,jsonify
from pytube import YouTube
import os,sys

import tkinter as tk
from threading import Thread
import webview


# Constants
executable_dir = os.path.dirname(sys.executable)
path_to_downloaded = os.path.join(executable_dir, 'downloaded')

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response

@app.route('/')
def menu():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json

    if data['url'] != None:
        try:
            url = data['url']
            if "youtu.be" in data['url']:
                url = url.split("?")[0]

            yt = YouTube(url)

            if os.path.exists(os.path.join(path_to_downloaded,f"{yt.title}.mp4")):
                return jsonify({'error': 'Video already downloaded!'}),400

            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=path_to_downloaded)
            return jsonify({'path': path_to_downloaded + "\\"+yt.title + ".mp4"}),200
        except Exception as e:
            return jsonify({'error': e}),400
    else:
        return jsonify({'error': 'URL not found'}),404

def run_server():
    app.run(host="0.0.0.0", port=5000)

root = tk.Tk()
root.title('Youtube Downloader by upio')

server = Thread(target=run_server)
server.daemon = True
server.start()

webview.create_window("Youtube Downloader by upio", "http://localhost:5000", width=500, height=700, resizable=True, fullscreen=False, min_size=(800, 600), confirm_close=False)
webview.start()

root.mainloop()