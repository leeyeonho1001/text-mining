#!/usr/bin/env python3
# coding: utf-8

import sys
import get_morphs_tags as mf

###############################################################################
def get_index_terms(mt_list):
    index_terms = []  #색인어 리스트
    compound = []  #현재 복합어를 구성하는 단일어 리스트
    sl = False #복합어의 SL 처리

    single_pos = {'NNG', 'NNP', 'SH'}
    compound_pos = {'NNG', 'NNP', 'NR', 'NNB', 'SL', 'SH', 'SN'}

    for morph, tag in mt_list:
        if tag in single_pos:
            index_terms.append(morph)
            compound.append(morph)
            if tag == 'SL':
                sl = True

        elif tag in compound_pos:
            compound.append(morph)
            if tag == 'SL':
                sl = True

        if tag not in compound_pos:
            if compound:
                if len(compound) >= 2:
                    index_terms.append(''.join(compound))
                elif sl == True:
                    index_terms.append(compound[0])
                    
                sl = False
                compound = []

    if compound:
        if len(compound) >= 2:
            index_terms.append(''.join(compound))
        elif sl == True:
            index_terms.append(compound[0])

    return index_terms

###############################################################################
# Converting POS tagged corpus to a context file
def tagged2context( input_file, output_file):
    try:
        fin = open( input_file, "r")
    except:
        print( "File open error: ", input_file, file=sys.stderr)
        sys.exit()

    try:
        fout = open( output_file, "w")
    except:
        print( "File open error: ", output_file, file=sys.stderr)
        sys.exit()

    for line in fin.readlines():
    
        # 빈 라인 (문장 경계)
        if line[0] == '\n':
            print("", file=fout)
            continue

        try:
            ej, tagged = line.split(sep='\t')
        except:
            print(line, file=sys.stderr)
            continue

        # 형태소, 품사 추출
        # return : list of tuples
        result = mf.get_morphs_tags(tagged.rstrip())
        
        # 색인어 추출
        # return : list
        terms = get_index_terms(result) 
        
        # 색인어 출력
        for term in terms:
            print(term, end=" ", file=fout)
        
    fin.close()
    fout.close()
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".context"
        print( 'processing %s -> %s' %(input_file, output_file), file=sys.stderr)
        
        # 형태소 분석 파일 -> 문맥 파일
        tagged2context( input_file, output_file)