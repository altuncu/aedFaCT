import re

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

"""
def get_abstract_summary(abstract, keywords):
    summary = ""
    sents = sent_tokenize(abstract)
    for sentence in sents:
        if any(word in sentence for word in keywords):
            for word in keywords:
                if word in sentence:
                    sentence.replace(word, "<mark>" + word + "</mark>")
            summary += sentence + " ... "
    return summary
"""

