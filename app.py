import os, sys, subprocess, math, time, secrets
import datetime, webbrowser, threading, json
from flask import (Flask, render_template, request, 
    redirect, url_for, send_from_directory, flash, jsonify
)
from src.utils import utils
from src.downloader.data_manager import DataManager


app = Flask(__name__, template_folder="templates")
# Generate random secret at startup (no need to keep user session data)
app.secret_key = secrets.token_hex(16)              

data_manager = DataManager(
    config_path = utils.getSettingsPath(), 
    db_path = utils.getDBPath()
)

def open_browser():
    time.sleep(1.5) 
    webbrowser.open("http://127.0.0.1:5000/settings")

DOWNLOADER_STATE = {
    "running": False
}

def run_downloader_background(app_context):

    with app_context:
        DOWNLOADER_STATE["running"] = True
        try:
            project_root = os.path.dirname(os.path.abspath(__file__))
            env = os.environ.copy()
            env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

            subprocess.run(
                [sys.executable, utils.getDownloaderPath()], 
                check=True,
                capture_output=False,
                cwd=project_root,
                env=env
            )
            
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_manager.set_last_run(now_str)
            print(f"Downloader finished successfully at {now_str}")
            
        except subprocess.CalledProcessError as e:
            print(f"Downloader script failed with return code {e.returncode}")
        except Exception as e:
            print(f"Error running downloader: {e}")
        finally:
            DOWNLOADER_STATE["running"] = False


# --- ENDPOINTS ---

@app.route('/')
def home():

    try:
        posts_per_page = data_manager.get_settings().get("post_per_page", 10)

        search_query = request.args.get('q', '')
        subreddit_filter = request.args.get('sub', '')
        page = int(request.args.get('page', 1))
        offset = (page - 1) * posts_per_page

        try:
            posts = data_manager.get_posts_paginated(
                limit=posts_per_page, 
                offset=offset, 
                query=search_query, 
                subreddit=subreddit_filter
            )
            for post in posts:
                if post['post_type'] != "text":
                    post['local_media'] = utils.getMediaPath(post['id'], post['post_type'] == "gallery")
            total_posts = data_manager.get_post_count(search_query, subreddit_filter)
        except Exception as e:
            print(f"Database access error: {e}")
            posts = []
            total_posts = 0    

        total_pages = math.ceil(total_posts / posts_per_page)

        return render_template(
            'index.html', 
            posts=posts, 
            page=page, 
            total_pages=total_pages,
            q=search_query,
            sub=subreddit_filter,
            last_run=data_manager.get_last_run()
        )
    except Exception as e:
        return render_template(
            'error.html', 
            error=e,
        )


@app.route('/post/<post_id>')
def view_post(post_id):

    try:
        post_meta = data_manager.get_post_by_id(post_id)
        if not post_meta:
            return render_template('error.html', message="Post not found"), 404

        comments = utils.getCommentsForPost(post_id)
        local_media_path = utils.getMediaPath(post_id, post_meta['post_type'] == "gallery")

        return render_template(
            'post.html', 
            post=post_meta, 
            comments=comments,
            local_media=local_media_path
        )
    except Exception as e:
        return render_template(
            'error.html', 
            error=e,
        )


@app.route('/media/<path:filename>')
def serve_media(filename):
    return send_from_directory(utils.getMediaDirectory(), filename)


@app.route('/status')
def status():
    return jsonify({
        "running": DOWNLOADER_STATE["running"],
        "last_run": data_manager.get_last_run()
    })


@app.route('/settings', methods=['GET', 'POST'])
def settings():

    if request.method == 'POST':
        try:
            json_data = request.form.get('subreddits_json')
            if json_data:
                new_settings = json.loads(json_data)
                data_manager.save_json_settings(new_settings)
                flash("Settings saved successfully!", "success")
            else:
                flash("No subreddit settings found to save.", "warning")

            new_configs = {
                "delete_older_than": request.form.get('delete_time'),
                "posts_per_page": request.form.get('posts_per_page')
            }
            data_manager.set_settings(new_configs)

            if request.form.get('action') == 'run_downloader':
                if not DOWNLOADER_STATE["running"]:
                    thread = threading.Thread(target=run_downloader_background, args=(app.app_context(),))
                    thread.start()
                    flash("Downloader started in background.", "info")
                else:
                    flash("Downloader is already running.", "warning")

            return redirect(url_for('settings'))
        
        except Exception as e:
            return render_template('error.html', error=e)
    
    # GET Request
    try:
        return render_template('settings.html', 
                    settings=data_manager.load_json_settings(),
                    last_run=data_manager.get_last_run(),
                    configs=data_manager.get_settings()
                )
    except Exception as e:
        return render_template('error.html', error=e)
    

@app.route('/delete', methods=['POST'])
def delete():
    try:
        data_manager.cleanup(True)
        return jsonify({
            "success": True, 
            "message": "Posts deleted successfully at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"[ERROR] Something went wrong when deleting posts: {str(e)}"
        }), 500
    

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


if __name__ == '__main__':
    if not os.path.exists(utils.getDBPath()):
        print("Database not found. Running setup...")
        subprocess.call([sys.executable, '-m', 'src.utils.setup'])
    
    threading.Thread(target=open_browser).start()
    app.run(debug=True, use_reloader=False)