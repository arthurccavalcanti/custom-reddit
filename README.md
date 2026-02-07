# Reddit Extractor

This is a web application to download and display content from reddit.com
- choose which subreddits to download from
- choose criteria for downloading posts
- store and manage posts locally

<gif here>


---
### How to use it

Once the app starts, you can choose **general settings**:
- `Deletion threshold`
	- after how many days should downloaded posts be deleted
- `Posts per page`
	- how many posts should be displayed in a page
	- (avoids doom scrolling)

You can also choose **subreddit-specific settings**:
- `Max posts`
	- maximum number of posts to be downloaded
- `Sort by`
	- order of selecting posts to be downloaded
	- for example, '5', 'new', will download the five most recent posts
- `Filter flairs`
	- whether to filter posts by flairs
		- ex. chooseing 'animals' and 'funny' will download only posts which have the 'animals' or 'funny' flairs
- `Ignore stickied posts`
	- whether to download or not posts which are fixed in their subreddit
- `Max comments`
	- how many comments to fetch from a post
- `Max replies`
	- how many replies to fetch from each comment
	- works recursively (i.e., setting max replies to 2 will fetch 2 replies for each reply, and so on)
- `Ignore stickied`
	- whether to fetch posts which are fixed in its comment section
- `Ignore post (comments)`
	- whether to ignore posts if they have fewer comments than the established threshold

Once you have decided on your preferred settings, you can run the downloader program and browse the app as if you were browsing regular reddit.


---
### How to run it

#### 1. Install a [python3 interpreter](https://www.python.org/downloads/) (if you don't have one installed)
- Make sure you can access python in your favourite CLI
- This should return the version you've downloaded
	- `> python3 --version`

#### 2. \[Optional step] Create a separate python environment
- This will isolate this program's dependencies
- It is useful if you wish to execute other python programs in the same computer
	- Creates an environment in the current directory called 'reddit_env': 
		- `> python3 -m venv reddit_env`
	- Activates this environment
		- In macOS/Linux:
			- `> source reddit_env/bin/activate`
	- In Windows: 
		- `> reddit_env\Scripts\activate`

#### 3. Install the app's dependencies
- Using pip in your CLI
	- `> pip install flask`
	- `> pip install moviepy`
	- `> pip install send2trash`
- You can also download the dependencies directly from the requirements.txt file
	- `> pip download -r requirements.txt`


#### 4. Navigate to the app's directory and execute it
- Navigate to wherever directory the project is at:
	-  `cd project_directory`
- Run the app 
	- `> python3 app.py`
- Once started, the app will open your browser in the app's settings page

---
### Wishlist of future features/changes

- Improve the pages' UI
- Style OP comments differently
- Add more specific downloader configurations
- Improve handling of unexistant subreddit names

---
### Boring technical details

#### Posts are stored in a local SQLite DB. 
- Here's the schema used:
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

GLOBAL_SETTINGS
	id INTEGER PRIMARY KEY,
	posts_per_page INTEGER,
	delete_older_than INTEGER,
	last_run TEXT
```

#### The .json file used to store a post's comments:
```json
{
	"id": str,
	"author": str,
	"score": str
	"body": str,
	"datetime": datetime,
	"replies": {
		"reply_id": {
			...
		}
	}

	// ... other comments
}
```

#### The .json file used to store each subreddit's download settings:
```json
{
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

  // ... other settings

}
```