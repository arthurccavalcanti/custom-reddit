import datetime
from typing import Dict, List
from src.downloader.storage.storage_comments import storage_comments

def comment_handler(post_comments: Dict, post_id: str, comment_params: Dict) -> str:

    comment_path = None
    processed_comments = {}

    if post_comments['data']['children']:
        top_comments = post_comments['data']['children']
        max_replies = comment_params["max_replies"]

        top_comments = process_comment_tree(top_comments, comment_params["max_comments"],
                                            None, comment_params["ignore_stickied_comments"])
        
        for top_comment in top_comments:
            comment_dict = format_comment(top_comment)
            comment_dict["replies"] = parse_replies_recursive(top_comment, max_replies)   
            processed_comments[top_comment['id']] = comment_dict

    comment_path = storage_comments(processed_comments, post_id)

    return comment_path


def process_comment_tree(comments: List[Dict], 
                         max_count: int,
                         parent_id: str = None, 
                         ignore_stickied: bool = True):
    
    results = []
    for comment in comments:
        if len(results) >= max_count:
            break

        comment_data = comment['data']
        if comment_data.get("author") is None or (comment_data['stickied'] and ignore_stickied):
            continue

        if parent_id is None:
            # Root comments' parent ID follows the format 't3_submissionID'
            if not comment_data['parent_id'].startswith('t3_'):
                continue

        results.append(comment_data)

    return results


def parse_replies_recursive(parent_comment: Dict, max_replies: int) -> Dict:

    replies_dict = {}
    if parent_comment['replies']:
        replies = process_comment_tree(parent_comment['replies']['data']['children'],
                                        max_replies,
                                        f"t1_{parent_comment['id']}")

        for reply in replies:
            reply_dict = format_comment(reply)
            reply_dict["replies"] = parse_replies_recursive(reply, max_replies)
            replies_dict[reply['id']] = reply_dict

    return replies_dict


def format_comment(comment: Dict) -> Dict:
    return {
        "author": str(comment['author']),
        "score": int(comment['score']),
        "body": comment['body'],
        "datetime": str(datetime.datetime.fromtimestamp(comment['created_utc'])),
        "id": comment['id']
    }