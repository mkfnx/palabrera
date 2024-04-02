import json
import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stopwords import stopwords
from stopwords_complement import default_stopwords_complement

TRANSCRIPTS_PATH = './scrapping/transcripts/'
FREQUENCY_MAPS_PATH = 'public/graphs/frequency_maps/'
TOP_WORDS_PATH = 'public/graphs/top_words/'
WORD_CLOUDS_PATH = 'public/graphs/wordclouds/'
BAR_CHARTS_PATH = 'public/graphs/barcharts/'


def create_stop_words_list(stopwords_complement):
    stopwords.update(default_stopwords_complement)
    stopwords.update(stopwords_complement)

    if stopwords_complement and len(stopwords_complement) > 0:
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
    for i in range(10):
        top_words_list.append(sorted_frequencies[i][0])

    new_file_name = file_name.replace('.txt', '.json')
    with open(f'{save_path}{new_file_name}', 'w', encoding='utf-8') as f:
        f.write(json.dumps(top_words_list, ensure_ascii=False))


def create_outputs(transcripts, stopwords_complement=None):
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

            save_frequency_map(FREQUENCY_MAPS_PATH, transcript_file_name, word_frequencies)
            save_top_words(TOP_WORDS_PATH, transcript_file_name, word_frequencies)

            file_name = transcript_file_name.replace('.txt', '.png')
            save_wordcloud(wordcloud, word_frequencies, WORD_CLOUDS_PATH, file_name)
            save_barchart(word_frequencies, BAR_CHARTS_PATH, file_name, 10)

            print(f'processed: {i + 1}')


if __name__ == "__main__":
    # create_outputs(['2024-04-01.txt'], ['cuevas', 'mujer'])
    create_outputs(
        os.listdir(TRANSCRIPTS_PATH)
    )
