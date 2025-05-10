# Extraindo comentários.
import datetime
import praw
from praw.models.reddit.more import MoreComments
import os
from dotenv import load_dotenv


def comment_handler(submission_url, max_comments=5, max_replies=3, less_comments=1):

    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')

    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent='reddit_comment_parser')

    submission = reddit.submission(url=submission_url)
    submission.comment_sort = 'top'

    comments_dict = {}

    top_comments = process_comment_tree(submission.comments, max_comments)

    for top_comment in top_comments:

        root_data = format_comment(top_comment)
        
        if less_comments:
            replies_dict = {}
            parent_id_str = f"t1_{top_comment.id}"
            replies = process_comment_tree(top_comment.replies, max_replies, parent_id_str)

            for reply in replies:                                           
                if reply.stickied or reply.author is None:          
                    continue
                reply_data = format_comment(reply)
                replies_dict[reply.id] = [reply_data, {}]

            comments_dict[top_comment.id] = [root_data, replies_dict]
        else:
            replies = parse_replies_recursive(top_comment, max_replies)   
            comments_dict[top_comment.id] = [root_data, replies]

    return comments_dict


# -----------------------

def process_comment_tree(comment_forest, max_count, parent_id_str=None):
    results = []
    queue = list(comment_forest)

    while queue and len(results) < max_count:
        item = queue.pop(0)

        if item.stickied or item.author is None:
            continue

        if isinstance(item, MoreComments):
            try:
                extra_comments = item.comments()
                queue = extra_comments + queue   
            except Exception as e:
                print(f"Error resolving MoreComments: {e}")
            continue

        if parent_id_str is not None and item.parent_id != parent_id_str:
            continue

        results.append(item)

    return results


# ------------------------

def parse_replies_recursive(comment, max_replies):

    replies_dict = {}

    parent_id_str = f"t1_{comment.id}"
    replies = process_comment_tree(comment.replies, max_replies, parent_id_str)

    for reply in replies:
        reply_data = format_comment(reply)
        nested = parse_replies_recursive(reply, max_replies)
        replies_dict[reply.id] = [reply_data, nested]

    return replies_dict


# -----------------------------------

def format_comment(comment):

    return [
        str(comment.author) if comment.author is not None else "[deleted]",         
        comment.score,
        comment.body,
        str(datetime.datetime.fromtimestamp(comment.created_utc))
    ]

# -----------------------------------

if __name__ == "__main__":
    test_url = 'https://www.reddit.com/r/NoStupidQuestions/comments/1k7g0ti/could_you_hide_your_immortality/'
    post_comments = comment_handler(test_url, 50,5)
