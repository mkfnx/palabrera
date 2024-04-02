import os
import json

frequency_maps_path = 'public/graphs/frequency_maps'
top_words_path = 'public/graphs/top_words'
fml = os.listdir(frequency_maps_path)

if __name__ == '__main__':
    for f in fml:
        print(f)
        file_name = f'{frequency_maps_path}/{f}'
        with open(file_name, 'r') as of:
            jc = json.loads(of.read())
            t = jc.items()
            st = sorted(t, key=lambda x: x[1], reverse=True)
            tw = []
            for i in range(10):
                tw.append(st[i][0])

            json_output_file = f'{top_words_path}/{f}'
            with open(json_output_file, 'w') as jof:
                js = json.dumps(tw)
                jof.write(js)
