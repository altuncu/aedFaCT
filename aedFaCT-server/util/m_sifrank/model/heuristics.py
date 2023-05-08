import csv
from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions
from collections import Counter
import nltk
from util.context_classifier import context_classifier as cc

def extract_noun_phrases(text):
        grammar = r"""
            NBAR:
                {<NN.*|JJ|VBG|VBN|CD>*<NN.*|VBG>}  # Nouns and Adjectives, terminated with Nouns

            NP:
                {<NBAR|JJ>}
                {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        """
        noun_phrases = set()
        sentences_str = [ [w for w in split_contractions(web_tokenizer(s)) if not (w.startswith("'") and len(w) > 1) and len(w) > 0] for s in list(split_multi(text)) if len(s.strip()) > 0]
        sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
        chunker = nltk.RegexpParser(grammar)
        toks = nltk.regexp_tokenize(text, sentence_re)
        postoks = nltk.tag.pos_tag(toks)
        tree = chunker.parse(postoks)
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            noun_phrases.add(" ".join([w[0] for w in subtree.leaves()]).lower())
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NBAR'):
            string = " ".join([w[0] for w in subtree.leaves()])
            noun_phrases.add(string.split(" ")[-1].lower())
            while len(string.split(" ")) > 1:
                string = string.split(" ", 1)[1]
                noun_phrases.add(string.lower())
        return noun_phrases

def second(kw):
    return kw[1]

def binary_search(file, term):
    file.seek(0, 2)
    size = file.tell()
    if size <= 0: 
        return False
    begin, end, middle = 0, size - 1, 1
    while begin < end:
        middle = (begin + end) >> 1
        if middle > 0:
            file.seek(middle)
            file.readline()
            line = file.readline()
        else:
            file.seek(0)
            line = file.readline()
        if line.rstrip('\n') == term: return True
        if not line or term < line.rstrip('\n'):
            end = middle
        else:
            begin = middle + 1
    return False

def apply_heuristics(input, keywords):
    kw_list = [list(e) for e in keywords]   
    
    noun_phrases = extract_noun_phrases(input)
    for kw in kw_list:
        if kw[0].lower() not in noun_phrases:
            kw_list.remove(kw)

    context = cc.predict_tags(input)
    if 'cs' in context:
        f = open('util/data/cso.txt', 'r', encoding='utf8')
        for kw in kw_list:
            if binary_search(f, kw[0].lower()):
                kw[1] = kw[1] * 2
        f.close()
    elif 'bio' in context:
        f = open('util/data/mesh.txt', 'r', encoding='utf8')
        for kw in kw_list:
            if binary_search(f, kw[0].lower()):
                kw[1] = kw[1] * 2
        f.close()
    elif 'fin' in context:
        f = open('util/data/stw.txt', 'r', encoding='utf8')
        for kw in kw_list:
            if binary_search(f, kw[0].lower()):
                kw[1] = kw[1] * 2
        f.close()
            
    wiki_f = open('util/data/wiki.txt', 'r', encoding='utf8', errors='ignore')
    for kw in kw_list:
        if binary_search(wiki_f, kw[0].lower()):
            kw[1] = kw[1] * 2
    wiki_f.close()
    
    kw_list.sort(key=second, reverse=True)

    return [tuple(e) for e in kw_list]    
