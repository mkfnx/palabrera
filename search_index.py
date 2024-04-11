import json
import os
from paths import *


def clean_search_term(search_term):
    search_term = search_term.strip().lower()
    tildes = 'áéíóú'
    no_tildes = 'aeiou'
    return search_term.translate(str.maketrans(tildes, no_tildes))


def build_search_index():
    search_index = {}

    for top_words_file_name in os.listdir(f'{TOP_WORDS_PATH}'):

        # skip files that don't have standard date format name
        if len(top_words_file_name) != 15:
            continue

        with open(f'{TOP_WORDS_PATH}{top_words_file_name}', 'r') as top_words_file:
            top_words = json.load(top_words_file)
            for w in top_words:
                w = clean_search_term(w)

                dates_list = search_index.get(w, [])
                dates_list.append(top_words_file_name.replace('.json', ''))
                search_index[w] = dates_list

    return search_index


if __name__ == '__main__':
    search_index = build_search_index()
    with open('public/search_index.json', 'w', encoding='utf-8') as output_file:
        json.dump(search_index, output_file, ensure_ascii=False)
