#!/usr/bin/env python3
# coding: utf-8

import sys
from collections import defaultdict

def word_count_by_year(filenames):
    word_freq_by_year = defaultdict(list)

    all_years = set()

    for filename in filenames:
        year = int(filename.split(".")[0])
        all_years.add(year)
        with open(filename, "r", encoding="utf-8") as fin:
            word_freq = defaultdict(int)
            for word in fin.read().split():
                word_freq[word] += 1
            for word, freq in sorted(word_freq.items()):
                word_freq_by_year[word].append((year, freq))

    for word, year_freq_list in word_freq_by_year.items():
        existing_years = {year for year, _ in year_freq_list}
        missing_years = all_years - existing_years
        for missing_year in missing_years:
            word_freq_by_year[word].append((missing_year, 0))

    for word, year_freq_list in word_freq_by_year.items():
        word_freq_by_year[word] = sorted(year_freq_list, key=lambda x: x[0])

    return word_freq_by_year


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s) > out-file", file=sys.stderr)
        sys.exit()

    input_files = sys.argv[1:]
    word_freq_by_year = word_count_by_year(input_files)

    for word, year_freq_list in sorted(word_freq_by_year.items()):
        frequencies = [freq for year, freq in year_freq_list]
        print("%s\t%s" % (word, frequencies))


