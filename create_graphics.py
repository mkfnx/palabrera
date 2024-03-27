import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from stopwords import stopwords
from stopwords_complement import default_stopwords_complement

TRANSCRIPTS_PATH = './scrapping/transcripts/'
FREQUENCY_MAPS_PATH = 'public/graphs/frequency_maps/'
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
    with open(f'{save_path}{file_name}', 'w') as f:
        f.write(str(frequency_map))


def create_outputs():
    wordcloud = word_cloud_with_stopwords()

    # transcripts = os.listdir(TRANSCRIPTS_PATH)
    transcripts = ['2024-03-27.txt']
    print(f'generate graphs for {len(transcripts)} transcripts')

    for i, transcript_file_name in enumerate(transcripts):
        with open(f'{TRANSCRIPTS_PATH}{transcript_file_name}') as transcript:
            print(transcript_file_name)
            if not transcript_file_name.endswith('.txt'):
                continue

            text = transcript.read()
            word_frequencies = wordcloud.process_text(text)

            save_frequency_map(FREQUENCY_MAPS_PATH, transcript_file_name, word_frequencies)

            file_name = transcript_file_name.replace('.txt', '.png')
            save_wordcloud(wordcloud, word_frequencies, WORD_CLOUDS_PATH, file_name)
            save_barchart(word_frequencies, BAR_CHARTS_PATH, file_name, 10)

            print(f'processed: {i + 1}')


if __name__ == "__main__":
    create_outputs()
