# Checks folders with data and deletes folders/files older than specificed amount of days.
import os
import time
from datetime import datetime, timedelta
import send2trash

"""
Deletes (moves to recycle bin) all folders and files inside folder_path 
that were last modified more than days_old days ago.
"""

def cleanup(days=None, output_folder=None):

    print(f"I will delete any folders or files in {output_folder} older than {days} days.")

'''
def delete_old_files_and_folders(folder_path, days_old):
    
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    now = time.time()
    cutoff_time = now - (days_old * 86400)  # 86400 seconds in a day

    deleted_items = []

    for root, dirs, files in os.walk(folder_path, topdown=False):
        # First delete old files
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    send2trash.send2trash(file_path)
                    deleted_items.append(str(file_path))

            except Exception as e:
                print(f"Failed to process file {file_path}: {e}")

        # Then delete old folders (after files inside have been deleted)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                dir_mtime = os.path.getmtime(dir_path)
                if dir_mtime < cutoff_time:
                    send2trash.send2trash(dir_path)
                    deleted_item.append(f"folder: {dir_path})

            except Exception as e:
                print(f"Failed to process folder {dir_path}: {e}")

    # TO DO: logger with deleted_items.
'''



if __name__ == "__main__":
    cleanup()
    '''
    import argparse

    parser = argparse.ArgumentParser(description="Delete old files and folders safely.")
    parser.add_argument("folder", help="Path to the input folder")
    parser.add_argument("days", type=int, help="Delete items older than this number of days")

    args = parser.parse_args()

    delete_old_files_and_folders(args.folder, args.days)
    '''