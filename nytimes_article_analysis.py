import csv
from collections import namedtuple
from datetime import date

CSV_FILENAME = "nytimes_headlines.csv"

Headline = namedtuple('Headline', ['title', 'date', 'url'])

def search_term(data: [], term: str) -> str:
    filtered_data = list(filter(lambda t: t[0].lower().find(term) > -1, data))
    sorted(filtered_data, key=lambda entry: entry[1])
    return filtered_data

def word_count(str_list: []):
    count = dict()
    for s in str_list:
        s.replace('’', '')
        s.replace('‘', '')
        letters = s.split()

        for letter in letters:
            try:
                count[letter] += 1
            except:
                count[letter] = 1
    return count

def load_list(fname: str) -> []:
    with open(CSV_FILENAME) as f:
        reader = csv.reader(f)
        return [ r for r in reader ]

def get_titles(headlines_data: []) -> []:
    return [ r[0] for r in headlines_data ]

if __name__ == "__main__":
    with open(CSV_FILENAME) as f:
        reader = csv.reader(f)

        hls = get_titles(load_list(CSV_FILENAME))

        print(len(hls))

        wc = word_count(hls)

        print(len(wc))

        for k, v in sorted(wc.items(), key=lambda i: i[1]):
            print("{}: {}".format(k, v))

