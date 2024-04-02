import os

TRANSCRIPTS_PATH = 'scrapping/transcripts'
BASE_PUBLIC_URL = "https://palabrera.info"

if __name__ == '__main__':
    url_list = [
        f'{BASE_PUBLIC_URL}/sobre_este_sitio',
        f'{BASE_PUBLIC_URL}/autor',
        f'{BASE_PUBLIC_URL}/aviso_de_privacidad',
    ]

    for fn in os.listdir(TRANSCRIPTS_PATH):
        url_path = fn.replace('.txt', '')
        url_list.append(f'{BASE_PUBLIC_URL}/conferencias_diarias/{url_path}')

    with open('public/sitemap.txt', 'w') as of:
        of.write('\n'.join(url_list))