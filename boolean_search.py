from __future__ import print_function
from word_parser import WordParser

SPECIAL_WORDS = 'specialwords.txt'


class BooleanSearch(object):
    """
    Boolean Search class
    Parses the input query and looks for the result files
    """
    def __init__(self, operators=None):
        """
        Constructor
        Sets the operators based on users preferences
        Sets the parser for word normalization
        """
        if operators:
            self.operators = operators
        else:
            self.operators = {
                'AND': 'and',
                'OR': 'or',
                'NOT': 'not'
            }
        # Normalizing middleware - really slow during tests
        self.parser = WordParser(SPECIAL_WORDS)
        self.searched_expressions = []

    def get_file_list(self, word_map, input_query, hasher, normalize=False):
        """
        The method returns lists of (file_list, to_find) tuples
        each tuple matching a searched word
        """
        file_collection = []
        for word, to_find in input_query:
            if normalize:
                word_id = str(
                    hasher(self.parser(word))
                )
            else:
                word_id = str(
                    hasher(word)
                )
            if word_id in word_map.keys():
                file_collection.append(
                    (word_map[word_id], to_find)
                )
            else:
                file_collection.append(
                    ([], to_find)
                )

        return file_collection

    def parse_input(self, input_query):
        """
        The input is parsed and the result is
        a list of lists - also indicating the priority of the boolean operators
         AND=NOT>OR
         each of the inner lists contain (word, negated) tuples to mark the NOT operator
        """
        query_list = []
        boolean_operator = ''
        for token in input_query:
            if token.lower() not in self.operators.values():
                if boolean_operator == self.operators['NOT']:
                    negated = True
                else:
                    negated = False
                query_list.append((token, negated))
            elif token.lower() == self.operators['OR']:
                boolean_operator = token.lower()
                self.searched_expressions.append(query_list)
                query_list = []
            else:
                boolean_operator = token.lower()
        self.searched_expressions.append(query_list)

    @staticmethod
    def evaluate_collection(collection):
        """
        Based on the file lists the method intersects or subtracts sets
        Reuniune pentru OR !!!!
        """
        result = set(collection[0][0])

        for file_list, negated in collection[1:]:
            if negated:
                result = result - set(file_list)
            else:
                result = result.intersection(set(file_list))

        return result

    def __call__(self, search_query, word_map, hasher=None):
        self.parse_input(search_query)
        doc_id_list = []

        for expression in self.searched_expressions:
            doc_id_list.append(
                self.evaluate_collection(
                    self.get_file_list(word_map, expression, hasher, True)
                )
            )

        # Union between all lists - OR
        union = doc_id_list[0]
        for item in doc_id_list[1:]:
            union = union.union(item)

        return union

