from typing import List, Dict
from src.utils import utils
from src.downloader.request_manager import RequestManager
from src.downloader.processing.handlers import media_handler, general_handler, comment_handler

def processor(posts: Dict, params: Dict, request_manager: RequestManager) -> List[Dict]:

    processed_posts = []

    for sub, posts_list in posts.items():

        sub_params = params.get(sub)
        for post in posts_list:

            post_data = post[0]['data']['children'][0]['data']
            post_comments = post[1]

            try:
                post_dict = general_handler.general_handler(post_data)
                post_dict['comments_path'] = comment_handler.comment_handler(post_comments, 
                                                                             post_data['id'],
                                                                             sub_params['comments'])

                if utils.is_image(post_data):
                    post_dict['image_path'] = media_handler.img_handler(post_data, request_manager)
                    post_dict['post_type'] = 'image'
                elif utils.is_video(post_data):
                    post_dict['video_path'] = media_handler.video_handler(post_data, request_manager)
                    post_dict['post_type'] = 'video'
                elif utils.is_gallery(post_data):
                    post_dict['gallery_path'] = media_handler.gallery_handler(post_data, request_manager)
                    post_dict['post_type'] = 'gallery'
                else:
                    post_dict['post_type'] = 'text'

                processed_posts.append(post_dict)
                print(f"Done processing post {post_dict["id"]}")

            except Exception as e:
                print(f"[ERROR] Error processing post {post_data['id']}: {e}")
                # log(f"Error when processing post {post['id']}.", e)
                continue

    return processed_posts