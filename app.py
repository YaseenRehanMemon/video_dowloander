from flask import Flask, request, jsonify, send_file, render_template, after_this_request
import yt_dlp
import os
import uuid

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

@app.route('/get_formats', methods=['POST'])
def get_formats():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # Show all video formats (with vcodec)
            formats = [
                {
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('resolution') or f.get('height'),
                    'format_note': f.get('format_note'),
                    'filesize': f.get('filesize')
                }
                for f in info['formats'] if f.get('vcodec') != 'none'
            ]
            return jsonify({'formats': formats, 'title': info.get('title', '')})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    from flask import after_this_request
    data = request.json
    url = data.get('url')
    format_id = data.get('format_id')
    if not url or not format_id:
        return jsonify({'error': 'Missing url or format_id'}), 400
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    # Always merge with bestaudio
    ydl_format = f"{format_id}+bestaudio"
    ydl_opts = {
        'format': ydl_format,
        'outtmpl': filepath,
        'quiet': True,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
    }
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