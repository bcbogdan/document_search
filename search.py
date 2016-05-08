from __future__ import print_function
import sys
import mmh3
from boolean_search import BooleanSearch
from vector_search import VectorSearch

INVERTED_INDEX_FILE = 'docs/reverse.txt'
DOCUMENTS_DICT = 'docs/documentIds.txt'
WORDS_DICT = 'docs/wordIds.txt'
DIRECT_INDEX_FILE = 'docs/index.txt'

DEFAULT_QUERY = ['program', 'string', 'word']


def get_word_id(word):
    """
    Hashing method
    """
    return mmh3.hash(word)


def create_map(file_path, dict_type):
    """
    Create a dictionary based on type
    - index (inverted or direct)
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
                    result_map[temp_word_id] = {}
                else:
                    result_map[temp_word_id][line_array[0]] = line_array[1]
            elif dict_type == 'dict':
                result_map[line_array[1]] = line_array[0]

    return result_map

if __name__ == '__main__':
    inverted_index_map = create_map(INVERTED_INDEX_FILE, 'index')
    direct_index_map = create_map(DIRECT_INDEX_FILE, 'index')
    documents_dict = create_map(DOCUMENTS_DICT, 'dict')
    words_dict = create_map(WORDS_DICT, 'dict')

    if len(sys.argv) == 1:
        query = DEFAULT_QUERY
    else:
        query = sys.argv[1:]

    vector_search = VectorSearch(documents_dict, words_dict, direct_index_map, inverted_index_map)

    result = vector_search(query, optimized=True)

    if not result:
        print('No document matches the search query')
    else:
        for doc_id, cos_value in result:
            print('%s - %s' % (documents_dict[doc_id], str(cos_value)))
