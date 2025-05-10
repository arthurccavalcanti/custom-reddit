import re
import os
import requests
import moviepy as mpe

def video_handler(post):

	# Checa se postagem tem URL do vídeo.
	if (post.media) or ('reddit_video' in post.media) or ('fallback_url' in post.media['reddit_video']):
			
		url_video = re.search(r"https://v.redd.it/\w+/\w+.mp4", post.media['reddit_video']['fallback_url'])
		if url_video:
			return url_video.group(0)
		else:
			raise(LookupError)
			logger("no fallback url")
	
	else:
		print("Couldn't find video's URL.")
		raise(LookupError)
		# TO DO: logger("no video url")

# -----------------------------------
'''
context = {'post_id': post_id, 'post_folder': post_folder_path}
video_data = 'url'

Para fazer o download do vídeo, temos que baixá-lo e baixar o áudio dele. Então, juntamos o vídeo e o aúdio.
Para acessar a URL do áudio, transformamos a URL do vídeo para o seguinte formato:
https://v.redd.it/{id}/DASH_AUDIO_{samplerate}.mp4
Por padrão, vamos usar samplerate = 128.

REGEX:
\d+ corresponde a dígitos decimais (Unicode).
\. corresponde ao ponto final (escape character + ponto).

Assim, transformamos a URL de, por exemplo, 'https://v.redd.it/1yboscka8jfe1/DASH_1080.mp4?source=fallback',
para a URL do aúdio: 'https://v.redd.it/1yboscka8jfe1/DASH_AUDIO_128.mp4?source=fallback'
'''
def video_storage(context, video_data):

	output_folder = context['post_folder']
	post_id = context['post_id']
	video_url = video_data

	# Determina nome provisório.
	video_file_name = f"{output_folder}/temp_video.mp4"
	audio_file_name = f"{output_folder}/temp_audio.mp4"

	# Determina nome final.
	output_file_name = f"video_{post_id}.mp4"

	# Tranforma URL do vídeo na URL do áudio.
	audio_url = re.sub(r'/DASH_\d+\.mp4', '/DASH_AUDIO_128.mp4', video_url)

	# Salva vídeo.
	with open(video_file_name, 'wb') as video_file:
		video_file.write(requests.get(video_url).content)

	# Salva áudio.
	with open(audio_file_name, 'wb') as audio_file:
		audio_file.write(requests.get(audio_url).content)

	# Estabelece clipes de áudio e vídeo.
	video_clip = mpe.VideoFileClip(video_file_name)
	audio_clip = mpe.AudioFileClip(audio_file_name)

	# Adiciona clipe de áudio ao vídeo.
	video_clip.audio = audio_clip.subclipped(0,video_clip.duration)

	# Usa atributo write_videofile() para salvar clipe final.
	video_clip.write_videofile(f"{output_folder}/{output_file_name}",fps=30, audio_codec="aac", audio_bitrate="128k")

	# Deleta arquivos temporários.
	os.remove(video_file_name)
	os.remove(audio_file_name)	


