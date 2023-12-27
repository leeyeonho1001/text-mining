#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math # sqrt

###############################################################################
def read_frequency(filename):
    freqs = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            freqs[parts[0]] = int(parts[1])
    return freqs

###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):
    t_scores = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            target_word = parts[0]
            cooc_word = parts[1]
            cooc_freq = int(parts[2])

            for a, b in (target_word, cooc_word), (cooc_word, target_word):
                if cooc_freq >= cutoff and a in unigrams and b in unigrams and b not in a:
                    expected_freq = (unigram_context[a] / uni_N) * unigrams[b]
                    t_score = (cooc_freq - expected_freq) / math.sqrt(cooc_freq)
                
                    if t_score > 0:
                        t_scores.append((a, b, t_score))

    t_scores.sort(key=lambda x: (x[0], x[1]))  # Sort by target word and then cooccurring word
    return t_scores

###############################################################################
def print_tscore(filename, t_scores):   
    with open(filename, 'w', encoding='utf-8') as file:
        for score in t_scores:
            file.write(f"{score[0]}\t{score[1]}\t{score[2]:.3f}\n")

###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산
    
    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"
    
        print("\tLoading %s.1gram" %file_stem, file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")
        
        print("\tLoading %s.1gram_context" %file_stem, file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")
        
        uni_N = unigrams['#Total'] # unigram 빈도 합
        
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)
        
        print_tscore(file_stem+".tscore", t_scores)

