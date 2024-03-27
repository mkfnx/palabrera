import json
import os
from datetime import datetime

start_date_str = '2018-12-04'


def renaming_moving_underscores(transcript):
    underscore_pos = transcript.find('_')

    if underscore_pos != -1:
        dot_pos = transcript.find('.')
        file_date = transcript[:dot_pos]
        underscores = transcript[underscore_pos:]

        origin_file = f'{transcripts_path}/{transcript}'
        destination_file = f'{transcripts_path}/{file_date}{underscores}.txt'

        os.rename(origin_file, destination_file)


if __name__ == '__main__':
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    # print(start_date)

    transcripts_path = f'{os.getcwd()}/transcripts'
    # print(transcripts_path)

    transcripts_by_date_dict = {}

    for transcript in os.listdir(transcripts_path):
        transcript_key = transcript.removesuffix('.txt').replace('_', '')

        date_transcripts = transcripts_by_date_dict.get(transcript_key, [])

        # transcript_value = transcript[transcript.find('_'):transcript.rfind('.')]
        date_transcripts.append(transcript)
        transcripts_by_date_dict[transcript_key] = date_transcripts

        with open('transcripts_by_date2.json', 'w') as output_file:
            json.dump(transcripts_by_date_dict, output_file)
