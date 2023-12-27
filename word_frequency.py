#!/usr/bin/env python3
# coding: utf-8

import sys
from collections import defaultdict

def word_count(filename):

    word_freq = defaultdict(int)

    with open(filename, "r", encoding='utf-8') as fin:
        for word in fin.read().split():
                word_freq[word] += 1
    
    return word_freq

    #word_freq=dict()

    #with open(filename, "r", encoding='utf-8') as fin:
        #for word in fin.read().split():
            #if word in word_freq:
                #word_freq[word]+=1
            #else:
                #word_freq[word]=1

if __name__ == "__main__":
    
    if len(sys.argv) <2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()
    
    for input_file in sys.argv[1:]:
        output_file = input_file + ".1gram"
        print('processing %s -> %s' %(input_file, output_file), file=sys.stderr)
        
        word_freq = word_count(input_file)
        
        with open(output_file, "wt", encoding='utf-8') as fout:
            #알파벳순 정렬
            for w, freq in sorted(word_freq.items()):
            #for w, freq in sorted(word_freq.items(),key=lambda x:x[1], reverse=True):
                print("%s\t%d" %(w, freq), file=fout)