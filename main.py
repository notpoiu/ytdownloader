from flask import Flask,render_template,request,jsonify
from mutagen.mp4 import MP4, MP4Cover
import pytube,os,requests,base64,re,sys

from threading import Thread
import webview

def safe_filename(filename):
    # Invlid_patterns was yoinked off of chatgpt, idk how to make regex
    invalid_patterns = [
        r'[#%&{}\\<>[*?$!/\'":@+`|=\-]',  # Matches any of the invalid characters, including '-' which should be escaped.
        r'\s+',                           # Matches any whitespace
        r'[^\x00-\x7F]+',                 # Matches any non-ASCII characters (emojis, alt codes, etc.)
    ]
    
    for pattern in invalid_patterns:
        filename = re.sub(pattern, '_', filename)
    
    return filename

def format_duration(seconds):
    total_seconds = round(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

# Constants
executable_dir = os.path.dirname(sys.executable) # when you are running from source, replace this with: os.path.dirname(os.path.realpath(__file__))
#executable_dir = os.path.dirname(os.path.realpath(__file__))
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


"""
/api/download

POST request
{
    "url": "https://www.youtube.com/watch?v=5qap5aO4i9A",
    "type": "mp4"
}
"""
@app.route('/api/download', methods=['POST'])
def download():
    data = request.json

    try:
        print(data)
        url = data['url']
        if "youtu.be" in url:
            url = url.split("?")[0]

        file_ext = data.get("type", "mp4")
        yt = pytube.YouTube(url)

        video_title = safe_filename(yt.title)
        file_path = os.path.join(path_to_downloaded, f"{video_title}.{file_ext}")

        if os.path.exists(file_path):
            return jsonify({'error': 'Video already downloaded!'}), 400

        yt.streams.filter(progressive=True, file_extension=file_ext).order_by('resolution').desc().first().download(output_path=path_to_downloaded, filename=f"{video_title}.{file_ext}")
        
        video = MP4(file_path)
        response = requests.get(yt.thumbnail_url)

        if response.status_code == 200:
            image_data = response.content
            video['covr'] = [MP4Cover(image_data, MP4Cover.FORMAT_JPEG)]
        else:
            raise Exception("Failed to download image")
        video.save()

        return jsonify({'path': file_path}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

"""
/api/getfiles

POST request
{
    "currentChildrenCount": videoListPopulate.children.length
}

returns a JSON list of files in downloaded folder, their thumbnail and name aswell as their media length
"""
@app.route('/api/getfiles', methods=['POST'])
def getfiles():
    files = []

    if not os.path.isdir(path_to_downloaded):
        os.mkdir(path_to_downloaded)

    if len(os.listdir(path_to_downloaded)) == 0:
        return jsonify({"message": "No files",'files': []}),200

    if request.json['currentChildrenCount'] == len(os.listdir(path_to_downloaded)):
        return jsonify({'message': "Same child count", 'files': []}),200

    for file in os.listdir(path_to_downloaded):
        if file.endswith(".mp4"):
            try:
                mp4 = MP4(os.path.join(path_to_downloaded, file))
                
                thumbnail_data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAyAAAAJYCAMAAACtqHJCAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAFQUExURWhoaAUFBVFRUZ6eng8PDxERERISEmpqamJiYhAQEJSUlJeXl1VVVSgoKBUVFZOTk7S0tKioqJmZmTQ0NBoaGiEhIT4+PnNzc6WlpZKSkl9fX2NjYyQkJGlpabOzswYGBqenp6CgoGdnZ6OjowcHB6ampnR0dFtbW21tbV5eXqSkpFhYWGZmZhQUFBMTE1ZWVpubm3JycmBgYCsrKycnJ1JSUgwMDAsLC3BwcFpaWjc3Nw4ODjU1NZ+fn2xsbFxcXAgICKurqw0NDbGxsVRUVKmpqaysrGVlZWtra1dXV05OTlNTU2FhYY+PjykpKYeHhzExMSwsLJiYmJqaml1dXVlZWQoKCmRkZHZ2dkhISCYmJiMjI62traGhoYiIiDIyMp2dnVBQUJycnJWVlZaWlkRERAkJCbKysq+vr5GRkQAAAAICAgEBAW9vb5CQkAAAAOiW2t0AAABwdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wC3YWLSAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAKjUlEQVR4Xu3d63cV1QHGYUfPiSZcpNqLhtKDiqLWBG89waYtCuINehEl1lZbq9YL1vL/fyvgdq2uFl8DnNl7j+t5PpB38pGs35rknJkzd10FvpNAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKB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AoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBAKBQCAQCAQCgUAgEAgEAoFAIBAIBALf6erV/wDqqp1SBzq0dgAAAABJRU5ErkJggg=="
                if 'covr' in mp4:
                    cover_data = mp4['covr'][0]
                    mime_type = "image/jpeg"
                    base64_encoded = base64.b64encode(cover_data).decode('utf-8')
                    thumbnail_data_uri = f"data:{mime_type};base64,{base64_encoded}"

                files.append({"name": file.replace("_"," ")[:-4], "thumbnail": thumbnail_data_uri, "length": format_duration(mp4.info.length)})
            except Exception as e:
                print(e)
                continue
    return jsonify({"message":"Success!",'files': files}),200

@app.route('/api/openfolder', methods=['GET'])
def openfolder():
    os.startfile(path_to_downloaded)
    return jsonify({'success': True}),200

def run_server():
    app.run(host="0.0.0.0", port=5000)

if not os.path.isdir(path_to_downloaded):
    os.mkdir(path_to_downloaded)

server = Thread(target=run_server)
server.daemon = True
server.start()

webview.create_window("Youtube Downloader by upio", "http://localhost:5000", width=500, height=700, resizable=True, fullscreen=False, min_size=(800, 600), confirm_close=False)
webview.start()

