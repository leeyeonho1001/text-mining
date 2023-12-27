#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt
from collections import defaultdict

###############################################################################
def cosine_similarity(t_vector, c_vector):
    dot_product = sum(t_vector[word] * c_vector[word] for word in t_vector if word in c_vector)
    norm_t = math.sqrt(sum(value ** 2 for value in t_vector.values()))
    norm_c = math.sqrt(sum(value ** 2 for value in c_vector.values()))

    if norm_t == 0 or norm_c == 0:
        return 0.0

    return dot_product / (norm_t * norm_c)
###############################################################################
def most_similar_words(word_vectors, target, topN=10):
    result = defaultdict(float)

    if target in word_vectors:
        target_vector = word_vectors[target]

        for context in target_vector:
            if context != target:
                for word, word_score in word_vectors[context].items():
                    similarity = cosine_similarity(target_vector, word_vectors[word])
                    if word != target and word not in target and similarity > 0.001:
                        result[word] = similarity

    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]

###############################################################################
def print_words(words):
    for word, score in words:
        print("%s\t%.3f" %(word, score))

###############################################################################
def search_most_similar_words(word_vectors, topN=10):

    print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    query = sys.stdin.readline().rstrip()

    while query:
        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN)
        
        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
        query = sys.stdin.readline().rstrip()
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    topN = 30
    
    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)
    
    search_most_similar_words(word_vectors, topN)
