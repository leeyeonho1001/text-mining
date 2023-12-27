#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations

###############################################################################
def get_word_freq(filename):
    word_freq = defaultdict(int)
    total_unigram_count = 0

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = set(line.strip().split())
            for word in words:
                word_freq[word] += 1
                total_unigram_count += 1

    return word_freq, total_unigram_count

###############################################################################
def print_word_freq(filename, word_freq, total_unigram_count=None):
    with open(filename, 'w', encoding='utf-8') as file:
        if total_unigram_count is not None:
            file.write("#Total\t{}\n".format(total_unigram_count))
        for word, freq in sorted(word_freq.items()):
            file.write(f"{word}\t{freq}\n")

###############################################################################
def get_coword_freq(filename):
    word_freq = defaultdict(int)
    coword_freq = defaultdict(int)
    word_context_size = defaultdict(int)

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.strip().split()
            unique_words = set(words)

            for word in unique_words:
                word_freq[word] += 1
                word_context_size[word] += len(unique_words)

            for pair in combinations(unique_words, 2):
                co_word_pair = tuple(sorted(pair))
                coword_freq[co_word_pair] += 1

    return word_freq, coword_freq, word_context_size

###############################################################################
def print_coword_freq(filename, coword_freq):
    with open(filename, 'w', encoding='utf-8') as file:
        for co_word_pair, freq in sorted(coword_freq.items()):
            file.write(f"{co_word_pair[0]}\t{co_word_pair[1]}\t{freq}\n")

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)
        
        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.tag.context" -> "2017"
        
        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem+".1gram", word_freq, total_unigram_count=sum(word_freq.values()))
        
        # bigram(co-word) 출력
        print_coword_freq(file_stem+".2gram", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem+".1gram_context", word_context_size)
