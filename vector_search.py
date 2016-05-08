from __future__ import print_function
from word_parser import WordParser
from collections import defaultdict
import mmh3
from math import log
from math import sqrt
import operator

SPECIAL_WORDS = 'specialwords.txt'


class VectorSearch(object):
    def __init__(self,  docs_map, words_map, direct_index_map, inverted_index_map, special_words=None):
        self.parser = WordParser(
            special_words if special_words else SPECIAL_WORDS
        )
        self.docs_map = docs_map
        self.words_map = words_map
        self.direct_index_map = direct_index_map
        self.inverted_index_map = inverted_index_map

    def __call__(self, query, optimized=False):

        # Reducing the document list
        if optimized:
            self.optimized_search_list(query)

        doc_vectors = self.get_doc_vectors(query)
        query_vector = self.get_query_vector(query)

        result = defaultdict(float)

        for document, vector in doc_vectors.iteritems():
            result[document] = self.get_cosine_similarity(vector, query_vector)

        result = sorted(result.items(), reverse=True, key=operator.itemgetter(1))

        return result

    def optimized_search_list(self, query):
        keys_to_remove = []
        for document, words in self.direct_index_map.iteritems():
            found = False
            for word in query:
                if str(mmh3.hash(word)) in words.keys():
                    found = True
            if not found:
                keys_to_remove.append(document)
        for key in keys_to_remove:
            del self.direct_index_map[key]

    def get_doc_vectors(self, query_words):
        result = defaultdict(list)
        for document, words in self.direct_index_map.iteritems():
            vector = []
            for word in query_words:
                try:
                    counter = self.inverted_index_map[
                        str(mmh3.hash(word))
                    ][document]
                except KeyError:
                    counter = 0

                if counter:
                    tf = int(counter) / float(len(words))
                    idf = log(len(self.direct_index_map.keys()) / float((1 + len(self.inverted_index_map[
                        str(mmh3.hash(word))
                                                                           ].keys()))))
                    vector.append(tf * idf)
                else:
                    vector.append(0)

            result[document] = vector

        return result

    @staticmethod
    def square_rooted(x):
        return round(
            sqrt(sum([a*a for a in x])), 3
        )

    @staticmethod
    def get_cosine_similarity(doc_vector, query_vector):
        numerator = sum(a*b for a,b in zip(doc_vector, query_vector))
        denominator = VectorSearch.square_rooted(doc_vector) * VectorSearch.square_rooted(query_vector)

        try:
            return round(
                numerator/float(denominator), 3
            )
        except ZeroDivisionError:
            return 0

    @staticmethod
    def get_query_vector(query_words):
        result = []
        for word in query_words:
            result.append(
                query_words.count(word) / float(len(query_words))
            )

        return result

    def evaluate_query(self):
        pass
