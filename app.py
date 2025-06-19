from flask import Flask, request, jsonify, send_file, render_template, after_this_request
import yt_dlp
import os
import uuid
import json

app = Flask(__name__, template_folder='templates')
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Global variable to store progress
progress_data = {'progress': 0, 'status': 'idle'}

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_data['progress'] = d.get('downloaded_bytes', 0) / max(d.get('total_bytes', 1), 1)
        progress_data['status'] = 'downloading'
    elif d['status'] == 'finished':
        progress_data['progress'] = 1.0
        progress_data['status'] = 'finished'
    elif d['status'] == 'error':
        progress_data['status'] = 'error'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    from flask import after_this_request
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing url'}), 400
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    ydl_opts = {
        'format': "bestvideo+bestaudio/best",
        'outtmpl': filepath,
        'quiet': True,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
    }

    # Check if running in production mode
    if os.environ.get('FLASK_DEBUG') == '0':
        ydl_opts['cookiesfrombrowser'] = ['chrome', 'firefox', 'safari']

    progress_data['progress'] = 0
    progress_data['status'] = 'downloading'
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        @after_this_request
        def remove_file(response):
            try:
                os.remove(filepath)
            except Exception:
                pass
            return response
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        progress_data['status'] = 'error'
        return jsonify({'error': str(e)}), 500
    finally:
        progress_data['status'] = 'idle'


@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress_data)

if __name__ == '__main__':
    app.run(debug=True)
