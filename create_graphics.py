import json
import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stopwords import stopwords
from stopwords_complement import default_stopwords_complement
from paths import *


def create_stop_words_list(stopwords_complement):
    stopwords.update(default_stopwords_complement)
    stopwords.update(stopwords_complement)

    return stopwords


def get_top_n_words(frequencies, n):
    top_words = {}
    frequencies_copy = frequencies.copy()
    for i in range(n):
        top_word = max(frequencies_copy, key=frequencies_copy.get)
        top_words[top_word] = frequencies_copy[top_word]
        del frequencies_copy[top_word]
    return top_words


def save_wordcloud(wordcloud, word_frequencies, save_path, file_name):
    fig1, ax1 = plt.subplots()
    ax1.imshow(wordcloud.generate_from_frequencies(word_frequencies), interpolation='bilinear')
    ax1.axis('off')
    fig1.savefig(f'{save_path}{file_name}')
    plt.close(fig1)


def save_barchart(word_frequencies, save_path, file_name, top_words_count=10):
    top_words = get_top_n_words(word_frequencies, top_words_count)
    top_words = dict(sorted(top_words.items(), key=lambda item: item[1]))
    words = list(top_words.keys())
    counts = list(top_words.values())

    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(9.6, 7.2)
    ax1.barh(words, counts)
    fig1.savefig(f'{save_path}{file_name}')
    plt.close(fig1)


def word_cloud_with_stopwords(stopwords_complement=None):
    if stopwords_complement is None:
        stopwords_complement = []
    sw_set = create_stop_words_list(stopwords_complement)
    return WordCloud(stopwords=sw_set, background_color='white',
                     width=800, height=400, min_font_size=8)


def save_frequency_map(save_path, file_name, frequency_map):
    new_file_name = file_name.replace('.txt', '.json')
    with open(f'{save_path}{new_file_name}', 'w', encoding='utf-8') as f:
        f.write(json.dumps(frequency_map, ensure_ascii=False))


def save_top_words(save_path, file_name, frequency_map):
    sorted_frequencies = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
    top_words_list = []
    total_words = len(sorted_frequencies) - 1
    max_words = total_words if total_words < 10 else 10
    for i in range(max_words):
        top_words_list.append(sorted_frequencies[i][0])

    if file_name.endswith('.txt'):
        new_file_name = file_name.replace('.txt', '.json')
    elif not file_name.endswith('.json'):
        new_file_name = file_name + '.json'
    else:
        new_file_name = file_name

    with open(f'{save_path}{new_file_name}', 'w', encoding='utf-8') as f:
        f.write(json.dumps(top_words_list, ensure_ascii=False))


def create_daily_outputs(transcripts, stopwords_complement=None):
    """
    Create charts (bar chart and word cloud) for each of the transcripts in the transcript list param
    :param transcripts: List of transcript filenames
    :param stopwords_complement: List of additional stopwords to be excluded
    :return: None.
    """
    wordcloud = word_cloud_with_stopwords(stopwords_complement)

    print(f'generate graphs for {len(transcripts)} transcripts')

    for i, transcript_file_name in enumerate(transcripts):
        with open(f'{TRANSCRIPTS_PATH}{transcript_file_name}') as transcript:
            print(transcript_file_name)
            if not transcript_file_name.endswith('.txt'):
                continue

            text = transcript.read()
            word_frequencies = wordcloud.process_text(text)

            # save_frequency_map(FREQUENCY_MAPS_PATH, transcript_file_name, word_frequencies)
            save_top_words(TOP_WORDS_PATH, transcript_file_name, word_frequencies)

            file_name = transcript_file_name.replace('.txt', '.png')
            # save_wordcloud(wordcloud, word_frequencies, WORD_CLOUDS_PATH, file_name)
            # save_barchart(word_frequencies, BAR_CHARTS_PATH, file_name, 10)

            print(f'processed: {i + 1}')


def create_aggregate_outputs(path, file_names, stopwords_complement=None):
    wordcloud = word_cloud_with_stopwords(stopwords_complement)

    for fn in file_names:
        if not fn.endswith('.json'):
            fn = fn + '.json'
        fn = f'{path}/{fn}'
        with open(fn) as file:
            aggregate_frequencies = json.load(file)

            # remove stopwords that are relevant in the aggregate but individually weren't
            for sw in stopwords_complement:
                del aggregate_frequencies[sw]

            file_name_parts = fn.split('/')
            output_file_path = '/'.join(file_name_parts[:-2])
            output_file_name = f'{file_name_parts[-1]}'

            save_top_words(f'{output_file_path}/top_words/', output_file_name, aggregate_frequencies)

            output_file_name = output_file_name.replace('.json', '.png')
            save_wordcloud(wordcloud, aggregate_frequencies, f'{output_file_path}/wordclouds/', output_file_name)
            save_barchart(aggregate_frequencies, f'{output_file_path}/barcharts/', output_file_name, 10)


if __name__ == "__main__":
    # Daily graphic
    # create_daily_outputs(
    #     ['2024-04-05.txt', '2024-04-08.txt', '2024-04-09.txt'],
    #     ['cuevas']
    # )

    # ALL GRAPHICS
    # create_outputs(
    #     os.listdir(TRANSCRIPTS_PATH)
    # )

    # YEAR AGGREGATE GRAPHICS
    # aggregate_frequencies_path = f'{AGGREGATES_YEAR_PATH}frequency_maps'
    # create_aggregate_outputs(
    #     aggregate_frequencies_path, os.listdir(aggregate_frequencies_path)
    # )

    # MONTH AGGREGATE GRAPHICS
    # aggregate_frequencies_path = f'{AGGREGATES_MONTH_PATH}frequency_maps'
    # create_aggregate_outputs(
    #     aggregate_frequencies_path, os.listdir(aggregate_frequencies_path)
    # )

    # WEEK AGGREGATE GRAPHICS
    # aggregate_frequencies_path = f'{AGGREGATES_WEEK_PATH}frequency_maps'
    # create_aggregate_outputs(
    #     aggregate_frequencies_path, os.listdir(aggregate_frequencies_path)
    # )

    # ALL TIME AGGREGATE GRAPHICS
    aggregate_frequencies_path = f'{AGGREGATES_ALL_TIME_PATH}frequency_maps'
    create_aggregate_outputs(
        aggregate_frequencies_path,
        ['all_time_data.json'],
        stopwords_complement=[
            'sólo', 'toda', 'bien', 'parte', 'mismo', 'importante', 'manera', 'hoy', 'tiempo', 'años', 'sino', 'seis',
            'primero', 'cuatro', 'vez', 'sido', 'primera', 'muchas', 'número', 'dio', 'todavía', 'ocho', 'lado', 'creo',
            'cuánto', 'través', 'cinco', 'segundo', 'cada', 'cuál', 'cabo', 'veces', 'hacia', 'digo', 'sigue', 'mal',
            'haciendo', 'incluso', 'tan', 'quiero', 'debe', 'dijo', 'iba', 'hizo', 'ir', 'acuerdo', 'quieren', 'dónde',
            'precisamente', 'puedo', 'podemos', 'favor', 'llevar', 'pueden', 'hablando', 'tipo', 'hicieron', 'algún',
            'después', 'cosa', 'aunque', 'respecto', 'pueda'
        ]
    )
