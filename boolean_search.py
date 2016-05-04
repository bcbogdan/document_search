from __future__ import print_function
import sys
import mmh3
from search import BooleanSearch

REVERSE_INDEX_FILE = 'docs/reverse.txt'
DOCUMENTS_DICT = 'docs/documentIds.txt'
DEFAULT_QUERY = ['document',  'AND', 'overview', 'NOT', 'unit', 'OR', 'secret', 'AND', 'handle']


def get_word_id(word):
    """
    Hashing method
    """
    return mmh3.hash(word)


def create_map(file_path, dict_type):
    """
    Create a dictionary based on type
    - index (reverse or direct)
    - dict (word/doc - word_id/doc_id)
    """
    result_map = {}
    temp_word_id = 'id'
    with open(file_path, 'r') as input_file:
        for line in input_file:
            line_array = line.strip().split(' ')
            if dict_type == 'index':
                if len(line_array) == 1:
                    temp_word_id = line_array[0]
                    result_map[temp_word_id] = []
                else:
                    result_map[temp_word_id].append(
                        line_array[0]
                    )
            elif dict_type == 'dict':
                result_map[line_array[1]] = line_array[0]

    return result_map

if __name__ == '__main__':
    word_map = create_map(REVERSE_INDEX_FILE, 'index')
    documents_dict = create_map(DOCUMENTS_DICT, 'dict')

    search = BooleanSearch()
    if len(sys.argv) == 1:
        query = DEFAULT_QUERY
    else:
        query = sys.argv[1:]

    doc_id_sets = search(query, word_map, get_word_id)

    for doc_id_set in doc_id_sets:
        for doc_id in doc_id_set:
            print(documents_dict[doc_id])
