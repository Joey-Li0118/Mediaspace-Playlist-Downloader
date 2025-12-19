# Mediaspace Video Playlist Downloader

## Setting up and Running
1. Activate and create a venv 

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install requirements
```
pip install -r requirements.txt
```
In addition, install ffmpeg through https://www.ffmpeg.org/download.html

3. Create your own .env file with this information

```
EMAIL = <your email>
PASSWORD = <your password>
PLAYLISTURL = <playlist url>
```

4. Run mediaspace.py

```
python mediaspace.py
```

5. Run download.py when ready to download the videos

```
python download.py
```
