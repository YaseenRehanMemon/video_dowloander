import os
import uuid

app = Flask(__name__, template_folder='templates')
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
=======
import os
import uuid
import json

app = Flask(__name__, template_folder='templates')
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
+++++++ REPLACE
------- SEARCH
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
=======
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
        cookies = [
            {
                "domain": ".youtube.com",
                "expirationDate": 1765914858.180423,
                "hostOnly": False,
                "httpOnly": True,
                "name": "VISITOR_PRIVACY_METADATA",
                "partitionKey": {
                    "hasCrossSiteAncestor": False,
                    "topLevelSite": "https://youtube.com"
                },
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "CgJQSxIEGgAgLw%3D%3D"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922822.80772,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__Secure-3PSID",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "g.a000yQiMSzkUoUSNXmpWGiX7-XatijzEr_SPdU29b4rpX75iZs3kMt3-FoGSUv3wopUttxal5AACgYKAeQSARcSFQHGX2Mie4_lOKuHZGEytlaZalHnQxoVAUF8yKqDa5UpedcZwqVJ6C8No3ez0076"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1781898846.593559,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__Secure-1PSIDTS",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "sidts-CjEB5H03PztC_6JPouMsTrGnf1Qq5CXWxFRCNcBErrttfwKteY64Il25V1oYvZdyivDZEAA"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922822.807727,
                "hostOnly": False,
                "httpOnly": False,
                "name": "SAPISID",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "p1ZUYIlfjq8fr8Db/A2FEHezeprrAfDlLx"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1781898858.180482,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__Secure-1PSIDCC",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "AKEyXzXmHeLJrFk64oknfQLg_tk5o_h5pCxHnuhwaVQvpWi59d_8v625vl30LPrWny4j0UqV"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922822.807724,
                "hostOnly": False,
                "httpOnly": True,
                "name": "SSID",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "A2hSvblYmntc10KOq"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922822.807729,
                "hostOnly": False,
                "httpOnly": False,
                "name": "__Secure-1PAPISID",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "p1ZUYIlfjq8fr8Db/A2FEHezeprrAfDlLx"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922822.807716,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__Secure-1PSID",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "g.a000yQiMSzkUoUSNXmpWGiX7-XatijzEr_SPdU29b4rpX75iZs3k42ysy8ok1L_elzrGFFyxHwACgYKAYQSARcSFQHGX2MisrZDabudJHNV_YOWEZH2PxoVAUF8yKr0IX1M7lMHXNlage81hCBj0076"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922822.807733,
                "hostOnly": False,
                "httpOnly": False,
                "name": "__Secure-3PAPISID",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "p1ZUYIlfjq8fr8Db/A2FEHezeprrAfDlLx"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1781898858.180503,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__Secure-3PSIDCC",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "AKEyXzX074D1JbQdvA4AzH5jWpwVTzszzMXN2VAgdSxkDZy1OTisQlzXO-Q0SP--ZHWd490HJXA"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1781898846.5937,
                "hostOnly": False,
                "httpOnly": True,
                "name": "__Secure-3PSIDTS",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "sidts-CjEB5H03PztC_6JPouMsTrGnf1Qq5CXWxFRCNcBErrttfwKteY64Il25V1oYvZdyivDZEAA"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922842.245204,
                "hostOnly": False,
                "httpOnly": True,
                "name": "LOGIN_INFO",
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "AFmmF2swRQIhAPyiQJx51OgzPg7AZqFOBO3af7k-kdfCBSE79XFbLntmAiAsciso_Vliyk5KwRTPbsIi9zyskciwuMZmkCTu5xoeLw:QUQ3MjNmeXVxeU13X1ZhNXdod0NRQmdvaGJlRlZuY0Y4TjVGNVZsTmN0anNXUkR4UDJUTnRtaF9feFUzZjRzdnZReGlOeExnUjVZVWs5OGluZ2E3ZjY2bDYxMzBkbGhaQzlteVU5ZXhfaFNvT1ZtRmlzVFgyTlp5bmMzYV9pY2JEVks0YUNFdWFtWlM2dU1WM3N4SU14QTlWcFJPeXBTcHNB"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1784922841.247376,
                "hostOnly": False,
                "httpOnly": False,
                "name": "PREF",
                "path": "/",
                "sameSite": None,
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "f6=40000080&f7=4140&tz=Asia.Karachi&f4=10000&f5=20000"
            },
            {
                "domain": ".youtube.com",
                "expirationDate": 1765914858.180315,
                "hostOnly": False,
                "httpOnly": True,
                "name": "VISITOR_INFO1_LIVE",
                "partitionKey": {
                    "hasCrossSiteAncestor": False,
                    "topLevelSite": "https://youtube.com"
                },
                "path": "/",
                "sameSite": "no_restriction",
                "secure": True,
                "session": False,
                "storeId": None,
                "value": "0HEG8Bkc9j4"
            }
        ]
        ydl_opts['cookiefile'] = 'cookies.txt'
        # Save cookies to file
        with open('cookies.txt', 'w') as f:
            for cookie in cookies:
                f.write(f"{cookie['domain']}\t{'TRUE' if cookie['hostOnly'] else 'FALSE'}\t{cookie['path']}\t{'TRUE' if cookie['secure'] else 'FALSE'}\t{cookie['expirationDate']}\t{cookie['name']}\t{cookie['value']}\n")

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
