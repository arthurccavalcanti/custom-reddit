import datetime
from typing import Dict, Callable

def general_handler(post: Dict) -> Dict:

    schema: Dict[str, tuple[str, Callable]] = {
        'subreddit':    ('subreddit', str),
        'title':        ('title', str),
        'text':         ('selftext', str),
        'ups':          ('ups', int),
        'downs':        ('downs', int),
        'flair':        ('link_flair_text', str),
        'author':       ('author', str),
        'num_comments': ('num_comments', int),
        'id':           ('id', str),
        'datetime':     ('created_utc', lambda x: datetime.datetime.fromtimestamp(x)),
        'url':          ('permalink', lambda x: f"https://www.reddit.com/{x}")
    }

    post_dict = {}

    for target_key, (source_key, transform) in schema.items():
        value = post.get(source_key)
        
        if value is None:
            if source_key == "link_flair_text":
                continue
            # log(f"Missing field: {source_key}")
            print(f"Field '{source_key}' is missing or None in {post.get("id")}")
            
        try:
            post_dict[target_key] = transform(value)
        except (ValueError, TypeError) as e:
            print(f"[ERROR] Error creating post dict {post}: {e}")
            # log(f"Conversion error for {target_key}: {e}")
            raise

    return post_dict