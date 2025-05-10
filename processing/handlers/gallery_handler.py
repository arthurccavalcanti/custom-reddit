# Salvando imagens de galerias.
import requests
import uuid


def gallery_handler(post):


    # Para cada galeria, vamos extrair as URLs das imagens dentro delas.
    # Primeiro, salvamos as extensões numa lista.
    # Na key de cada imagem, encontramos as extensões no value da key 'm' (ex. 'm':'image/jpg')
    # Limpamos o valor para extrair somente a extensão: "image/jpg" -> "jpg"

    # Extaindo URLs das imagens da galeria.
    url_list =[]

    try:
        # Cria lista das extensões de arquivo das imagens.
        extensions = []
        for image_id, value in post['data']['media_metadata'].items():
            extensions.append(value["m"].split("/")[-1])
            
        # Cria lista das IDs das imagens.
        image_ids = [id for id in post["data"]["media_metadata"]]

        # Adiciona à lista URLs com IDs e extensões seguindo este formato de URL: 'https://i.redd.it/01vb7df95ree1.jpg'
        for i, extension in enumerate(extensions):
            url_list.append(f"https://i.redd.it/{image_ids[i]}.{extension}")

    except AttributeError:
        print("Couldn't extract gallery URLS.")
        # TO DO: logger("A imagem foi deletada", post['title'])

    return url_list

# ----------------------------
'''
context = {'post_id': post_id, 'post_folder': post_folder_path}
gallery_data = [url1, url2, ...]
'''
def gallery_storage(context, gallery_data):

    for url in gallery_data:

        # Gets extension from URL: 'https://i.redd.it/01vb7df95ree1.jpg' -> 'jpg'
        extension = url.rsplit('.',1)[1]

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
        file_path = f"{folder}/gallery_{unique_id}.{extension}"

        with open(file_path, 'wb') as handler:
            handler.write(req.content)
            print(f'Imagem {url} salva em {file_path}')
            # TO DO: logger
