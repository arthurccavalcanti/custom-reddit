from src.downloader.request_manager import RequestManager
from src.downloader.processing.processor import processor
from src.downloader.data_manager import DataManager
from src.utils.utils import getSettingsPath, getDBPath

def main():

    data_manager = DataManager(
        config_path=getSettingsPath(), 
        db_path=getDBPath()
    )
    request_manager = RequestManager()

    params = data_manager.load_json_settings()

    try:
        posts = request_manager.get_posts(params)
    except Exception as e:
        print(f"[ERROR] Something went wrong when fetching posts: {e}")
        # log("Error when fetching post", e)
        raise

    try:
        processed_posts = processor(posts, params, request_manager)
    except Exception as e:
        print(f"ERROR] Something went wrong when processing posts: {e}")
        # log("Error when processing post", e)
        raise

    for post in processed_posts:
        try:
            data_manager.add(post)
        except Exception as e:
            print(f"[ERROR] Something went wrong when saving post {post[id]}: {e}")
            # log("Error when storing post", e)
            raise
    
    try:
        data_manager.cleanup(None)
    except Exception as e:
        # log("Error when cleaning up", e)
        print(f"[ERROR] Something went wrong when deleting posts: {e}")
        raise

if __name__ == "__main__":
    main()