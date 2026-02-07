import os
import glob
import json
from typing import Dict

def is_image(post: Dict):
    if 'post_hint' in post and post['post_hint'] == 'image':
        return True
    return False

def is_gallery(post: Dict):
    if 'is_gallery' in post and post['is_gallery']:
        return True
    return False
    
def is_video(post: Dict):
    return post['is_video']

def sanitize_filename(name: str):
    return "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in name).strip()

def getCommentsForPost(post_id: str):
    file_path = os.path.join(getCommentsDirectory(), f"{post_id}.json")
    if not os.path.exists(file_path):
        return []
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading comments for {post_id}: {e}")
        # log("Error loading comments.", e)
        return []


# -- PATH HELPERS --

def getLogsDirectory():
    return os.path.join(getProjectRootPath(), 'data', 'logs')

def getCommentsDirectory():
    return os.path.join(getProjectRootPath(), 'data', 'posts_comments')

def getMediaDirectory():
    return os.path.join(getProjectRootPath(), 'data', 'posts_media')

def getDBPath():
    return os.path.join(getProjectRootPath(), 'data', 'reddit.db')

def getSettingsPath():
    return os.path.join(getProjectRootPath(), 'data', 'params.json')

def getDownloaderPath():
    return os.path.join(getProjectRootPath(), 'src', 'downloader', 'main.py')

def getProjectRootPath():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def getMediaPath(post_id: str, isGallery: bool):
    search_pattern = os.path.join(getMediaDirectory(), f"{post_id}*.*")
    matches = glob.glob(search_pattern)
    if matches and isGallery:
        return [os.path.basename(path) for path in matches]

    elif matches:
        return os.path.basename(matches[0])
    
    return None