import os

files = os.listdir('./transcripts')

for file in files:
    name_parts = file.split('.')
    if len(name_parts) != 4:
        continue

    day = name_parts[0]
    month = name_parts[1]
    year = name_parts[2]

    os.rename(f'./transcripts/{file}', f'./transcripts/20{year}-{month}-{day}.txt')