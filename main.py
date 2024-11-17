import csv
import json
import re

CSV_FILE = 'result.csv'
CSV_HEADERS = ['author', 'first 3-gram', 'second 3-gram', 'third 3-gram', 'fourth 3-gram', 'fifth 3-gram']


def get_three_gram(s):
    res = re.findall(r'\b\w+\b', s.lower())
    return ' '.join(res[:3])


def read_json_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
    return content


def write_csv(dict):
    with open(CSV_FILE, 'w', encoding='utf-8', newline='') as _file:
        writer = csv.DictWriter(_file, CSV_HEADERS)
        writer.writeheader()
        for k, v in dict.items():
            v = v + [""] * (5 - len(v))  # Fill None elements with empty str
            writer.writerow({
                'author': k,
                'first 3-gram': v[0],
                'second 3-gram': v[1],
                'third 3-gram': v[2],
                'fourth 3-gram': v[3],
                'fifth 3-gram': v[4]
            })

def process_json_file():
    dict_result = {}
    for line in read_json_file('10K.github.jsonl'):
        json_line = json.loads(line)
        author = json_line['actor']['login']

        if json_line['type'] == 'PushEvent':
            payload = json_line['payload']

            if 'commits' in payload:
                for single_commit in payload['commits']:
                    _3_gram = get_three_gram(single_commit['message'])

                    if author not in dict_result:
                        dict_result[author] = [_3_gram]
                    else:
                        if len(dict_result[author]) < 5:
                            dict_result[author].append(_3_gram)
    return dict_result


if __name__ == '__main__':
    parsed_result = process_json_file()
    write_csv(parsed_result)
