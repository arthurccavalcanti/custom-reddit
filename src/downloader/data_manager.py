import json
import os
import sqlite3
import time
from src.utils.utils import getCommentsDirectory, getMediaDirectory
from src.downloader.storage.cleanup import delete_dir

class DataManager:
    
    def __init__(self, config_path, db_path):
        self.config_path = config_path
        self.db_path = db_path

    # --- Subreddit Settings ---

    def load_json_settings(self):
        if not os.path.exists(self.config_path):
            print(f"Couldn't save settings because {self.config_path} wasn't found")
            raise Exception
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_json_settings(self, settings):
        with open(self.config_path, 'w') as f:
            json.dump(settings, f, indent=4)

    # --- SQL ---

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        return conn
    
    def get_posts_paginated(self, limit, offset, query=None, subreddit=None):
        conn = self._get_db_connection()
        sql = "SELECT * FROM posts WHERE 1=1"
        params = []

        if subreddit:
            sql += " AND subreddit LIKE ?"
            params.append(f"%{subreddit}%")
        
        if query:
            sql += " AND title LIKE ?"
            params.append(f"%{query}%")

        sql += " ORDER BY datetime DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        posts = conn.execute(sql, params).fetchall()
        conn.close()
        return [dict(post) for post in posts]

    def get_post_count(self, query=None, subreddit=None):
        conn = self._get_db_connection()
        sql = "SELECT COUNT(*) FROM posts WHERE 1=1"
        params = []

        if subreddit:
            sql += " AND subreddit LIKE ?"
            params.append(f"%{subreddit}%")
        
        if query:
            sql += " AND title LIKE ?"
            params.append(f"%{query}%")

        count = conn.execute(sql, params).fetchone()[0]
        conn.close()
        return count

    def get_post_by_id(self, post_id):
        conn = self._get_db_connection()
        post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        conn.close()
        return dict(post) if post else None
    
    def delete_older_than(self, cutoff_unix_time):
        conn = self._get_db_connection()
        try:
            conn.execute("DELETE FROM posts WHERE strftime('%s', datetime) + 0 < ?", (cutoff_unix_time,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error deleting old posts: {e}")
        finally:
            conn.close()

    def add(self, post):
        if self.get_post_by_id(post.get('id')):
            return

        conn = self._get_db_connection()
        try:
            columns = list(post.keys())
            values = tuple(post.values())

            placeholders = ", ".join(["?"] * len(columns))
            column_names = ", ".join(columns)

            sql = f"INSERT INTO POSTS ({column_names}) VALUES ({placeholders})"
            conn.execute(sql, values)
            conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error adding post {post.get('id')}: {e}")
        finally:
            conn.close()

    # --- SQL Settings ---

    def get_settings(self):
        conn = self._get_db_connection()
        settings = conn.execute("SELECT * FROM global_settings").fetchone()
        conn.close()
        return dict(settings) if settings else None
    
    def set_settings(self, settings):
        try:
            if int(settings["posts_per_page"]) <= 0 or int(settings["delete_older_than"]) < 0:
                raise Exception
        except:
            print("Invalid settings. Ignoring...")
            return
        conn = self._get_db_connection()
        conn.execute("UPDATE global_settings SET posts_per_page = ?, delete_older_than = ?", (settings["posts_per_page"], settings["delete_older_than"]))
        conn.commit()
        conn.close()
    
    def get_last_run(self):
        conn = self._get_db_connection()
        last_run = conn.execute("SELECT last_run FROM global_settings").fetchone()
        conn.close()
        return last_run[0] if last_run else "Never"

    def set_last_run(self, timestamp_str):
        conn = self._get_db_connection()
        conn.execute("UPDATE global_settings SET last_run = ?", (timestamp_str,))
        conn.commit()
        conn.close()

    # --- Cleanup ---

    def cleanup(self, delete_all):

        media_dir = getMediaDirectory()
        comments_dir = getCommentsDirectory()

        if delete_all:
            now = time.time()
            delete_dir(media_dir, now)
            delete_dir(comments_dir, now)
            self.delete_older_than(now)
        else:
            threshold = self.get_settings()["delete_older_than"]
            if threshold:
                cutoff_time = time.time() - (int(threshold) * 86400)  # 86400 seconds in a day
                delete_dir(media_dir, cutoff_time)
                delete_dir(comments_dir, cutoff_time)
                self.delete_older_than(cutoff_time)
                # log("Cleanup completed.")
            else:
                print("[WARN] Threshold not found")