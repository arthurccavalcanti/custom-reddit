from src.downloader.request_manager import RequestManager
from src.downloader.storage import storage_media
import re
from typing import Dict, List

def img_handler(post: Dict, request_manager: RequestManager) -> str:
    try:
        img_url = post['url_overridden_by_dest']
        file_extension = img_url.split(".")[-1]
        if file_extension.lower() not in ["png", "jpg", "jpeg", "gif"]:
            # log("Image extension not supported.")
            raise Exception("Image extension not supported.") 
        
        print(f"Fetching image {img_url} for {post["id"]}")
        img_bytes = request_manager.download_media(img_url)
        return storage_media.image_storage(img_bytes, post['id'], file_extension)
    
    except Exception as e:
        print(f"[ERROR] Error fetching image from {post['id']}: {e}")
        # log("Error when fetching post image URL.", e)
        raise

def gallery_handler(post: Dict, request_manager: RequestManager) -> str:
    try:
        url_list = get_gallery_urls(post)
        path_list = []
        for index, url in enumerate(url_list):
            file_extension = url.split(".")[-1]
            
            print(f"Fetching image {url} for {post["id"]}")
            img_bytes = request_manager.download_media(url)
            path_list.append(storage_media.image_storage(img_bytes, post['id'] + str(index), file_extension))
        return ", ".join(path_list)
    
    except Exception as e:
        print(f"[ERROR] Error fetching gallery from {post['id']}: {e}")
        # log("Error when fetching post gallery URLs.", e)
        raise

def video_handler(post: Dict, request_manager: RequestManager) -> str:
    try:
        has_audio = post['media']['reddit_video']['has_audio']

        url_regex = re.search(r"https://v.redd.it/\w+/\w+.mp4", post['media']['reddit_video']['fallback_url'])
        if not url_regex:
            raise Exception("Couldn't find video URL")
        video_url = url_regex.group(0)
        
        print(f"Fetching audio and video {video_url} for {post["id"]}")
        video_bytes = request_manager.download_media(video_url)
        audio_bytes = None

        if has_audio:
            audio_pattern_dash = re.search(r'/DASH_\d+\.mp4', video_url)
            audio_pattern_cmaf = re.search(r'/CMAF_\d+\.mp4', video_url)
            if audio_pattern_dash:
                audio_url = re.sub(r'/DASH_\d+\.mp4', '/DASH_AUDIO_128.mp4', video_url)
            elif audio_pattern_cmaf:
                audio_url = re.sub(r'/CMAF_\d+\.mp4', '/CMAF_AUDIO_128.mp4', video_url)
            else:
                raise Exception("Couldn't find audio URL")
            
            audio_bytes = request_manager.download_media(audio_url)

        return storage_media.video_storage(audio_bytes, video_bytes, post['id'])

    except Exception as e:
        print(f"[ERROR] Error fetching video from {post['id']}: {e}")
        # log("Error when fetching post video URL.", e)
        raise

def get_gallery_urls(post: Dict) -> List[str]:
    url_list =[]
    extensions = []     # Extensions are found in 'm' (ex. 'm':'image/jpg')
    for value in post['media_metadata'].values():
        extensions.append(value["m"].split("/")[-1])
        
    image_ids = [id for id in post["media_metadata"]]
    for i, extension in enumerate(extensions):
        url_list.append(f"https://i.redd.it/{image_ids[i]}.{extension}")

    return url_list