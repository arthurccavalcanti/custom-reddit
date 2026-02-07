import moviepy as mpe
import os
from src.utils.utils import getMediaDirectory, sanitize_filename
import os

def image_storage(img_bytes, post_id, file_extension):
	file_name = sanitize_filename(post_id)
	file_path = os.path.join(getMediaDirectory(), f"{file_name}.{file_extension}")
	
	if not os.path.exists(file_path):
		with open(file_path, 'wb') as f:
			f.write(img_bytes)
		return file_path
	else:
		print(f"Image already exists: {file_name}")
		return file_path


def video_storage(audio_bytes, video_bytes, post_id):
    
	media_dir = getMediaDirectory()
	file_name = sanitize_filename(post_id)      
	output_file_path = os.path.join(media_dir, f"{file_name}.mp4")
      
	if not os.path.exists(output_file_path):

		temp_video_file_path = os.path.join(media_dir, "temp_video.mp4")
		temp_audio_file_path = os.path.join(media_dir, "temp_audio.mp3")

		try:
			if not audio_bytes:
				with open(output_file_path, 'wb') as video_file:
					video_file.write(video_bytes)
			else:
			
				with open(temp_video_file_path, 'wb') as video_file:
					video_file.write(video_bytes)

				with open(temp_audio_file_path, 'wb') as audio_file:
					audio_file.write(audio_bytes)
					
				video_clip = mpe.VideoFileClip(temp_video_file_path)
				audio_clip = mpe.AudioFileClip(temp_audio_file_path)

				# Calculate the shortest duration between the two clips
				min_duration = min(video_clip.duration, audio_clip.duration)

				# Trim both clips to the minimum duration
				video_clip = video_clip.subclipped(0, min_duration)
				audio_clip = audio_clip.subclipped(0, min_duration)

				video_clip.audio = audio_clip
				video_clip.write_videofile(
					output_file_path, 
					fps=30, 
					audio_codec="aac", 
					audio_bitrate="128k",
					logger=None
				)
				
				# Close clips to release file handles
				video_clip.close()
				audio_clip.close()

		except Exception as e:
			print(f"[ERROR] Error processing video {post_id}: {e}")
			if os.path.exists(output_file_path):
				os.remove(output_file_path) # Cleanup failed output
			raise e
		finally:
			# Cleanup temp files
			if os.path.exists(temp_video_file_path):
				os.remove(temp_video_file_path)
			if os.path.exists(temp_audio_file_path):
				os.remove(temp_audio_file_path)
		
		return output_file_path
	
	else:
		print(f"Video already exists: {file_name}. Skipping...")
		return output_file_path