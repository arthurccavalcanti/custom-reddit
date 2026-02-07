import os
import send2trash

def delete_dir(dir_name, cutoff_time):
    deleted_items = []
    for root, dirs, files in os.walk(dir_name, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    print(f"Deleting {file_path}")
                    send2trash.send2trash(file_path)
                    deleted_items.append(str(file_path))

            except Exception as e:
                # log(f"Failed to delete {file_path}", e)
                print((f"[ERROR] Failed to delete {file_path}", e))
                raise