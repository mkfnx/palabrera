import json
import os.path

import bs4
import requests

BASE_URL = 'https://presidente.gob.mx/secciones/version-estenografica/page/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/123.0.0.0 Safari/537.36',
}
last_page_number = 139


def save_article(article_content, file_path):
    with open(f'{file_path}', 'w') as f:
        print(f'contents: {len(article_content.contents)}')
        for p in article_content.children:
            f.write(p.text)


def parse_article(url):
    article_request = requests.get(url, headers=headers)
    article_html = article_request.text
    article_soup = bs4.BeautifulSoup(article_html, 'html.parser')

    article_title = article_soup.find('h1')
    if article_title:
        date_str = article_title.string.split(" ")[0]
    else:
        date_str = '[Sin título]'

    article_content = article_soup.find('div', class_='entry-content')

    return {
        'title': article_title.string,
        'content': article_content,
        'date': date_str
    }


def get_page_articles(url):
    """

    :param url: Url of the page to extract the articles from; A page number of the transcripts base URL.
    :return: list of BeautifulSoup article tags contained in the page
    """
    page_request = requests.get(url, headers=headers)
    page_html = page_request.text
    page_soup = bs4.BeautifulSoup(page_html, 'html.parser')

    return page_soup.find_all('article')


def get_file_paths(article_url, article_info):
    save_path = f'{os.getcwd()}/scrapping/transcripts/'
    date_parts = article_info["date"].split('.')
    if len(date_parts) == 3:
        file_name = f'20{date_parts[2]}-{date_parts[1]}-{date_parts[0]}'
    else:
        file_name = article_url.split('/')[-2]
    full_path = f'{save_path}{file_name}.txt'

    return file_name, full_path


def get_new_name_for_duplicated(file_path):
    dot_pos = file_path.find('.')
    file_name_left = file_path[:dot_pos]
    file_name_right = file_path[dot_pos:]

    return f'{file_name_left}_{file_name_right}'


def get_transcripts_data(articles):
    transcripts_by_date_dict = {}

    for i in range(len(articles), 0, -1):
        article_url = articles[i - 1].a.attrs['href']
        article_info = parse_article(article_url)

        file_name, file_path = get_file_paths(article_url, article_info)

        if file_name.find('_') == -1:
            date_key = file_name
        else:
            date_key = file_name[:file_name.find('_')]
        # if os.path.exists(file_path):
        #     file_name = get_new_name_for_duplicated(file_name)
        #     date_key = file_name[file_path.find('_')]

        date_articles = transcripts_by_date_dict.get(date_key, [])
        date_articles.append(
            {
                'file_name': file_name,
                'title': article_info['title'],
                'url': article_url
            }
        )
        transcripts_by_date_dict[date_key] = date_articles
        # save_article(
        #     article_info['content'],
        #     file_path
        # )

    return transcripts_by_date_dict


def scrap_all_conferences():
    transcripts_by_date_dict = {}
    for page_number in range(last_page_number, 0, -1):
        page_url = f'{BASE_URL}{page_number}'
        print(page_url)

        articles_info = get_transcripts_data(get_page_articles(page_url))
        transcripts_by_date_dict.update(articles_info)

    with open('transcripts_by_date3.json', 'w') as f:
        print('json dump')
        json.dump(transcripts_by_date_dict, f)


def save_articles(articles):
    """
    Save article contents to the file system
    :param articles: list of BeautifulSoup article tags contained in the page
    :return: None. Articles get saved to the file system in the predefined path (./scrapping/transcripts)
    """
    for i in range(len(articles), 0, -1):
        article_url = articles[i - 1].a.attrs['href']
        article_info = parse_article(article_url)

        file_name, file_path = get_file_paths(article_url, article_info)

        # TODO compare contents to decide if a new file should be created
        #  (this is the case when there's more than conference in one day)
        # if os.path.exists(file_path):
        #     file_name = get_new_name_for_duplicated(file_name)
        #     date_key = file_name[file_path.find('_')]

        save_article(
            article_info['content'],
            file_path
        )


if __name__ == '__main__':
    save_articles(
        get_page_articles(f'{BASE_URL}1')
    )
