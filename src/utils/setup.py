import os
import sqlite3
from src.utils.utils import (getProjectRootPath, getSettingsPath,
                            getCommentsDirectory, getMediaDirectory, getDBPath)

def setup_environment():

    data_dir = os.path.join(getProjectRootPath(), 'data')
    dirs = [data_dir, getCommentsDirectory(), getMediaDirectory()]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Checked/Created directory: {d}")

    if not os.path.exists(getSettingsPath()):
        with open(getSettingsPath(), 'w') as f:
            f.close()
        print("Created params.json file.")

    conn = sqlite3.connect(getDBPath())
    cursor = conn.cursor()
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            subreddit TEXT,
            text TEXT,
            datetime TIMESTAMP,
            num_comments INTEGER,
            ups INTEGER,
            downs INTEGER,
            url TEXT,
            post_type TEXT,
            image_path TEXT,
            gallery_path TEXT,
            video_path TEXT,
            comments_path TEXT,
            flair TEXT
        );
    """
    create_global_settings = """
        CREATE TABLE IF NOT EXISTS global_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            posts_per_page INTEGER,
            delete_older_than INTEGER,
            last_run TEXT
        );
    """
    insert_default_settings = """
        INSERT INTO global_settings (id, posts_per_page, delete_older_than, last_run)
        VALUES (1, 10, 7, "Never")
    """
    cursor.execute(create_table_sql)
    cursor.execute(create_global_settings)
    cursor.execute(insert_default_settings)
    conn.commit()
    conn.close()
    print(f"Database initialized at {getDBPath()}")
    # log("Setup completed")


if __name__ == "__main__":
    setup_environment()