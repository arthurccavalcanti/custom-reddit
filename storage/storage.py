# Receives data from handlers and creates folders and files.
import os
import json
import datetime
from gallery_handler import gallery_storage
from video_handler import video_storage
from img_handler import image_storage


'''
output_folder/subreddit_folder/date_folder/post_folder/post_data.json
processed_posts = [post_dict1, post_dict2, ...]

post_dict = {'comments':{comments},
            'subreddit': post['subreddit'],
            'title':post['title'],
            'text':post['selftext'],
            'ups':post['ups'],
            'downs':post['downs'],
            'flair':post['link_flair_text'],
            'author':post['author'],
            'num_comments':post['num_comments'],
            'datetime':datetime.datetime.fromtimestamp(int(post['created_utc'])),
            'url':f'https://www.reddit.com/{post['permalink']}',
            'post_type:'post_type',
            'id':'post_id',
            #OPTIONALS:
            'image':{image},
            'video':{video},
            'gallery:{gallery}
            }

1) Accesses a given output folder and iterates all subreddits in the processed posts.
2) Checks for every subreddit if there is a folder in the output folder with the subreddit's name.
3) If there isn't, creates a folder with the subreddit name.
4) For each subreddit folder, checks today's date and if there is a folder with today's date as its name.
5) If there isn't, creates a folder with today's date as its name.
6) For each date folder, checks its subreddit's posts IDs and see if there are folders whose name contains the IDs.
7) If there aren't, creates folders with the format: '{post title}_{post_id}'.
8) For each post, check its type and if it is a video, an image or a gallery, calls the appropriate function, such as video_storage(context, post['video']).
9) Saves each post in its appropriate folder as a JSON.
'''


#Removes or replaces invalid characters in folder names.
# test later!
def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in name).strip()  

# ------------------------------------------------------------------------

def reddit_local_storage(processed_posts=None, output_folder=None):

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    for post in processed_posts:

        subreddit = post['subreddit']
        post_id = post['id']
        post_title = sanitize_filename(post['title'])[:20]  # Truncated up to 20 characters.
        
        # 1) Create the subreddit folder if it doesn't exist
        subreddit_path = os.path.join(output_folder, subreddit)
        os.makedirs(subreddit_path, exist_ok=True)
        
        # 2) Create today's date folder inside subreddit folder
        date_path = os.path.join(subreddit_path, today_str)
        os.makedirs(date_path, exist_ok=True)

        # 3) Check if post folder already exists (using ID)
        post_folder_name = f"{post_title}_{post_id}"
        post_folder_path = os.path.join(date_path, post_folder_name)
        os.makedirs(post_folder_path, exist_ok=True)

        # 4) Check post type and handle media
        context = {'post_id': post_id, 'post_folder': post_folder_path}
        post_type = post.get('post_type')

        # If type matches and data exists, send data to appropriate handler.
        if post_type == 'video' and post.get('video'):
            video_storage(context, post['video'])
        elif post_type == 'image' and post.get('image'):
            image_storage(context, post['image'])
        elif post_type == 'gallery' and post.get('gallery'):
            gallery_storage(context, post['gallery'])
        else:
            print(f"No media to save for post {post_id}")
            # TO DO: logger

        # 5) Save post metadata as JSON
        json_path = os.path.join(post_folder_path, f"{post_folder_name}_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=4)

# --------------------------

if __name__ == "__main__":
    reddit_local_storage()