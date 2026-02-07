from src.utils.utils import sanitize_filename, getCommentsDirectory
import json, os
from typing import Dict

def storage_comments(comments: Dict, post_id: str):
    try:
        file_name = sanitize_filename(post_id)
        file_path = os.path.join(getCommentsDirectory(), f"{file_name}.json")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(comments, f, indent=4)
                # log("Comments saved", file_path, post_id)
            return file_path
        else:
            print(f"Comments already exists for {post_id}")
            return file_path
    except Exception as e:
        print(f"[ERROR] Something went wrong when saving comments: {e}")
        # log("Error when storing comments", e)
        raise