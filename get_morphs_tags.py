#!/usr/bin/env python3
# coding: utf-8

import sys

###############################################################################
def get_morphs_tags(tagged):
    result = []
    
    taggedmorphs = tagged.replace('+/SW', '♧/SW').split('+')

    for word in taggedmorphs:
        word = word.replace('♧', '+')
        morph, tag = word.split('/', 1) if '/' in word else (word, '')
        result.append((morph, tag))
        
    return result

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as fin:

        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2: 
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())
        
            for morph, tag in result:
                print(morph, tag, sep='\t')
