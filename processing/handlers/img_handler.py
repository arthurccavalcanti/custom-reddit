import requests
import uuid

def img_handler(post=None):

    img_url = post['data']['url_overridden_by_dest']
    file_extension = img_url.split(".")[-1]

    img_dict = {'url':post['data']['url_overridden_by_dest'], 'extension':file_extension}

    return img_dict

# ---------------------------------
'''
context = {'post_id': post_id, 'post_folder': post_folder_path}
image_data = {'url':url, 'extension':file_extension}
'''
def image_storage(context, image_data):

    url = image_data['url']
    extension = image_data['extension']
    req = requests.get(url)
    if not req.ok:
        raise Exception("Erro com URL da imagem.")
        # TO DO: logger

    if extension.lower() not in ["png", "jpg", "jpeg", "gif"]:
        print("Extensão não disponível")
        raise Exception("Erro com extensão da imagem.")
        # TO DO: logger

    folder = context['post_folder']
    unique_id = uuid.uuid4()
    file_path = f"{folder}/image_{unique_id}.{extension}"

    with open(file_path, 'wb') as handler:
        handler.write(req.content)
        print(f'Imagem {url} salva em {file_path}')
        # TO DO: logger


# ---------------------------------
if __name__ == '__main__':
    img_handler()