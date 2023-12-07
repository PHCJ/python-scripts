# -*- coding: utf-8 -*-
pip install youtube-transcript-api

pip install google-api-python-client

import googleapiclient.discovery

# Substitua 'SUA_CHAVE_DE_API' pela chave de API obtida no Google Developers Console
keyapi = 'chave do google API'

API_KEY = keyapi

# Lista de temas de interesse
temas = ["inteligência emocional", "controle de emoções", "controle de sentimentos", "lidar com emoções", "lidar com sentimentos"]

# Número desejado de vídeos por tema
num_videos_por_tema = 10

# Criação do serviço da API do YouTube
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

# Função para obter vídeos por tema
def obter_videos_por_tema(tema, quantidade):
    resultado = youtube.search().list(
        q=tema,
        type='video',
        part='id,snippet',
        maxResults=quantidade
    ).execute()

    videos = []
    for item in resultado['items']:
        video = {
            'titulo': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'url': f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        }
        videos.append(video)

    return videos

# Coleta de vídeos para cada tema
todos_os_videos = {}
for tema in temas:
    videos_do_tema = obter_videos_por_tema(tema, num_videos_por_tema)
    todos_os_videos[tema] = videos_do_tema

# Exibição dos resultados
for tema, videos in todos_os_videos.items():
    print(f'\nTema: {tema}')
    for video in videos:
        print(f'Título: {video["titulo"]}')
        print(f'URL: {video["url"]}')

from youtube_transcript_api import YouTubeTranscriptApi as yta
import os

videos = todos_os_videos
video_ids_todos_temas = []
# Itera sobre cada tema e seus vídeos
for tema, lista_videos in videos.items():
    # Extrai os video_ids e adiciona à lista
    video_ids_todos_temas.extend(video['video_id'] for video in lista_videos)
    #Cria as pastar por tema
    # Substitui espaços por underscores para criar nomes de pasta válidos
    #tema_folder = tema.replace(' ', '_')
    #os.makedirs(tema_folder, exist_ok=True)

def obter_transcricao(video_id):
  transcricao = []
  for id in video_id:
    try:
      transcricao.append(yta.get_transcript(id, languages=['pt','en']))
    except Exception as e:
      print(f"Erro ao obter transcrição para o vídeo {id}: {str(e)}")
      video_id.remove(id)
  return transcricao

data = obter_transcricao(video_ids_todos_temas)

#texto_completo = ' '.join([bloco['text'] for sublist in data for bloco in sublist])

os.makedirs('textos', exist_ok=True)

# Iterar sobre cada conjunto de dados e salvar em arquivos numerados
for idx, bloco in enumerate(data, start=1):
    # Juntar todos os textos do conjunto
    texto_completo = ' '.join(item['text'] for item in bloco)

    # Criar um nome de arquivo numerado
    nome_arquivo = f'texto_completo_{idx}.txt'

    # Caminho completo do arquivo, incluindo a pasta "textos"
    caminho_arquivo = os.path.join('textos', nome_arquivo)

    # Salvar em um arquivo de texto
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(texto_completo)

    print(f'Arquivo {nome_arquivo} salvo com sucesso.')

    # Adicionar uma quebra de linha entre os blocos
    print()  # Apenas para uma melhor formatação na saída

print('Todos os arquivos foram salvos.')

#Cria um arquivo zip chamado "pasta.zip" que contém todos os arquivos na pasta "textos".
#!zip -r pasta.zip textos