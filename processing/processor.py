# Receives responses and routes them to appropriate handlers.
import json
import pprint
'''
from comment_handler import comment_handler
from gallery_handler import gallery_handler
from img_handler import image_handler
from general_handler import general_handler
from video_handler import video_handler
'''

# Takes as input a list of responses [res1, res2, ...]
# and the parameters in the form of a list of tuples:
# [(subreddit1, dict_of_parameters), (subreddit2, dict_of_parameters), ...]

# Handlers return post as a dict {post_type:text, url:none, comment:[], replies:[], ...}

def processor(responses, params):

    processed_posts =[]

    for i in len(responses):

        # Parameters for each request.
        ignore_stickied_posts = params[i][1]['ignore_stickied_posts']
        ignore_fewer_comments = params[i][1]['ignore_fewer_comments']
        comments = params[i][1]['comments']
        replies = params[i][1]['replies']

        for post in responses[i].json()['data']['children']:

            if (post['stickied'] == True) and (ignore_stickied_posts == True):
                pass
            elif post['num_comments'] < ignore_fewer_comments:
                pass
            else:

                post_dict = general_handler(post)
                post_dict['comments'] = comment_handler(post_dict['url'], comments, replies)

                if is_image(post):
                    post_dict['image'] = image_handler(post)
                    post_dict['post_type'] = 'image'
                elif is_video(post):
                    post_dict['video'] = video_handler(post)
                    post_dict['post_type'] = 'video'
                elif is_gallery(post):
                    post_dict['gallery'] = gallery_handler(post)
                    post_dict['post_type'] = 'gallery'
                else:
                    post_dict['post_type'] = 'text'

                processed_posts.append(post_dict)

    return processed_posts

# -------------------------------------
# Checks if post is an imagem.

def is_image(post):

    if 'post_hint' in post['data'] and post['data']['post_hint'] == 'image':
        return True
    else:
        return False

# -------------------------------------
# Checks if post is a gallery.

def is_gallery(post):

    if 'is_gallery' in post['data'] and post['data']['is_gallery'] == True:
        return True
    else:
        return False
    

# ------------------------------------
# Check if post is a video.

def is_video(post):

    if post['is_video']:
        return True
    else:
        return False