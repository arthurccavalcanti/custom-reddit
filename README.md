## Instructions

- Make sure you have python installed, and python and pip commands available in your shell
	- `python3 --version`
	- `pip3 --version`

1. Navigate to wherever the project is `cd project_directory`
	1. Optionally, create a virtual environment
	- `python3 -m venv reddit_env`
	- macOS/Linux: 
		- `source reddit_env/bin/activate`
	- Windows: 
		- `reddit_env\Scripts\activate`
2. Install requirements `pip install -r requirements.txt`
3. Run the app `python3 app.py`


---
### Data Structures

```
POST
	id TEXT PRIMARY KEY,
	title TEXT,
	author TEXT,
	subreddit TEXT,
	text TEXT (optional),
	datetime REAL,
	num_comments INTEGER,
	ups INTEGER,
	downs INTEGER,
	url TEXT,
	post_type TEXT,
	image_path TEXT (optional),
	gallery_path TEXT (optional),
	video_path TEXT (optional),
	comment_path TEXT (optional),
	flair TEXT (optional)

COMMENT (.json)
	 "id": str
	 "author": str,
	 "score": str
	 "body": str,
	 "datetime": datetime,
	 "replies": {
		"reply_id": {
			...
		}
	 }

PARAMS (.json)
  "subreddit_name": {
    "num_posts": 7,
    "ignore_stickied_posts": false,
    "ignore_if_fewer_comments_than": 10,    
    "order_by": "hot",
    "flairs": {
      "filter": true,
      "wanted_flairs": ["flair1", "flair2"]
    },
    "comments": {
        "max_comments": 5,
        "max_replies": 2,
        "order_comments_by": "new",
        "ignore_stickied_comments": false
    }
  },
  ...
```