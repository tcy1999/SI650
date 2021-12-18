from pyserini.index import IndexReader
from tqdm import tqdm, trange
import sys
import numpy as np


class Ranker(object):
    '''
    The base class for ranking functions. Specific ranking functions should
    extend the score() function, which returns the relevance of a particular 
    document for a given query.
    '''
    def __init__(self, index_reader):
        self.index_reader = index_reader
        
        # common cached data to improve speed
        self.n = self.index_reader.stats()['non_empty_documents']
        self.avg_dl = 0
        self.doc_vectors = {}

        for i in range(self.n):
            doc_id = self.index_reader.convert_internal_docid_to_collection_docid(i)
            doc_id = str(doc_id)
            doc_vec = self.index_reader.get_document_vector(doc_id)
            # doc_raw = self.index_reader.doc_raw(doc_id)
            doc_len = sum([x for x in doc_vec.values() if x is not None])
            self.doc_vectors[doc_id] = (doc_vec, doc_len)
            self.avg_dl += doc_len

        self.avg_dl /= self.n


    def score(query, doc):        
        '''
        Returns the score for how relevant this document is to the provided query.
        Query is a tokenized list of query terms and doc_id is the identifier
        of the document in the index should be scored for this query.
        '''
        rank_score = 0
        return rank_score


class PivotedLengthNormalizatinRanker(Ranker):
    def __init__(self, index_reader):
        super(PivotedLengthNormalizatinRanker, self).__init__(index_reader)
        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)


    def score(self, query, doc_id):
        '''
        Scores the relevance of the document for the provided query using the
        Pivoted Length Normalization ranking method. Query is a tokenized list
        of query terms and doc_id is a numeric identifier of which document in the
        index should be scored for this query.
        '''
        rank_score = 0
        
        ###########################YOUR CODE GOES HERE######################
        #
        # TODO: Implement Pivoted Length Normalization here. You'll want to use
        # the information in the self.index_reader. This object will let you
        # convert the the query and document into vector space representations,
        # as well as count how many times the term appears across all documents.
        #
        # IMPORTANT NOTE: We want to see the actual equation implemented
        # below. You cannot use any of Pyserini's built-in BM25-related code for
        # your solution. If in doubt, check with us.
        #        
        # For some hints, see the IndexReader documentation:
        # https://github.com/castorini/pyserini/blob/master/docs/usage-indexreader.md
        #
        b = 0.6
        doc_vector, d = self.doc_vectors[doc_id]
        
        try:
            for term in query:
                if term in doc_vector:
                    df, _ = self.index_reader.get_term_counts(term)
                    rank_score += query[term] * (1 + np.log(1 + np.log(doc_vector[term]))) / (
                        1 - b + b * d / self.avg_dl) * np.log((self.n + 1) / df)
        except Exception:
            # some stop words, pass
            pass
        ###########################END OF CODE#############################
    
        return rank_score

    
class BM25Ranker(Ranker):
    def __init__(self, index_reader):
        super(BM25Ranker, self).__init__(index_reader)
        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)


    def score(self, query, doc_id, k1=1.2, b=0.75, k3=1.2):
        '''
        Scores the relevance of the document for the provided query using the
        BM25 ranking method. Query is a tokenized list of query terms and doc_id
        is a numeric identifier of which document in the index should be scored
        for this query.
        '''
        rank_score = 0
        
        ###########################YOUR CODE GOES HERE######################
        #
        # TODO: Implement BM25 here (using the equation from the slides). You'll
        # want to use the information in the self.index_reader. This object will
        # let you convert the the query and document into vector space
        # representations, as well as count how many times the term appears
        # across all documents.
        #
        # IMPORTANT NOTE: We want to see the actual equation implemented
        # below. You cannot use any of Pyserini's built-in BM25-related code for
        # your solution. If in doubt, check with us.
        #
        # For some hints, see the IndexReader documentation:
        # https://github.com/castorini/pyserini/blob/master/docs/usage-indexreader.md
        #
        doc_vector, d = self.doc_vectors[doc_id]
        k1 = 0.5  
        k3 = 2
        
        try:
            for term in query:
                if term in doc_vector:
                    df, _ = self.index_reader.get_term_counts(term)
                    rank_score += np.log((self.n - df + 0.5) / (df + 0.5)) * (k1 + 1) * doc_vector[term] / (
                        k1 * (1 - b + b * d / self.avg_dl) + doc_vector[term]) * (
                            k3 + 1) * query[term] / (k3 + query[term])
        except Exception:
            # some stop words, pass
            pass
        ###########################END OF CODE#############################

        return rank_score

    
class CustomRanker(Ranker):
    def __init__(self, index_reader):
        super(CustomRanker, self).__init__(index_reader)
        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)


    def score(self, query, doc_id):
        '''
        Scores the relevance of the document for the provided query using a
        custom ranking method. Query is a tokenized list of query terms and doc_id
        is a numeric identifier of which document in the index should be scored
        for this query.
        '''
        rank_score = 0
        
        ###########################YOUR CODE GOES HERE######################
        #
        # TODO: Implement your custome ranking function here. You'll want to use
        # the information in the self.index_reader. This object will let you
        # convert the the query and document into vector space representations,
        # as well as count how many times the term appears across all documents.
        #
        # IMPORTANT NOTE: We want to see the actual equation implemented
        # below. You cannot use any of Pyserini's built-in BM25-related code for
        # your solution. If in doubt, check with us.
        #
        # For some hints, see the IndexReader documentation:
        # https://github.com/castorini/pyserini/blob/master/docs/usage-indexreader.md
        #
        doc_vector, d = self.doc_vectors[doc_id]
        k = 7 
        b = 0.4 
        
        try:
            for term in query:
                if term in doc_vector:
                    df, _ = self.index_reader.get_term_counts(term)
                    rank_score +=  (k + 1) * query[term] / (k + query[term]) * (1 + np.log(np.sqrt(doc_vector[term]))) / (
                        1 - b + b * d / self.avg_dl) * np.log((self.n + np.log(df + 1)) / (df + 1))
        except Exception:
            # some stop words, pass
            pass
        ###########################END OF CODE#############################

        return rank_score
