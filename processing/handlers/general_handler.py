# Returns post's title, text, upvotes, downvotes, number of comments, author, subreddit, date, flair, post_type, and url
from datetime import datetime

def general_handler(post):

    post_dict = {'subreddit': post['subreddit'],
                'title':post['title'],
                'text':post['selftext'],
                'ups':post['ups'],
                'downs':post['downs'],
                'flair':post['link_flair_text'],
                'author':post['author'],
                'num_comments':post['num_comments'],
                'datetime':datetime.datetime.fromtimestamp(int(post['created_utc'])),
                'url':f'https://www.reddit.com/{post['permalink']}',
                'id':post['id'],
                } 
    
    return post_dict