from rankers import PivotedLengthNormalizatinRanker, BM25Ranker, CustomRanker
from pyserini.index import IndexReader
from tqdm import tqdm, trange
import sys
import pandas as pd
import numpy as np


def run_test(ranker):
    '''
    Prints the relevance scores of the top retrieved documents.
    '''
    # NOTE: You can extend this code to have the program read a list of queries
    # and generate rankings for each.   
    sample_query = 'nidoviru'
    print(
    "Score for term is ",
    ranker.score(
        sample_query.split(" "),
        '59087'))


def run_task(ranker, folder, top_num=5):
    query_reader = IndexReader(folder + '/indexes/query')
    if folder == 'covid':
        sorter = pd.read_csv(folder + '/sample_submission.csv')['QueryId']
    else:
        sorter = pd.read_csv(folder + '/' + folder + '_query_sample_submission.csv')['QueryId']
    indexes = np.unique(sorter, return_index=True)[1]
    query_id = [sorter[index] for index in sorted(indexes)]
    # query_df = pd.read_csv(folder + '/query.csv')
    ranking = []

    for id in query_id:
    # for id in range(query_reader.stats()['non_empty_documents']):
        # query = query_df.loc[id]['Query Description'].split()
        query = query_reader.get_document_vector(str(id))
        scores = {}
        for doc in ranker.doc_vectors:
            scores[doc] = ranker.score(query, doc)
        temp = sorted(scores, key=scores.get, reverse=True)[:top_num] 
        for doc_id in temp:
            ranking.append((id, doc_id))
    
    ranking_df = pd.DataFrame(ranking, columns=['QueryId', 'DocumentId'])
    ranking_df.to_csv(folder + '_submission.csv', index=False)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python main.py path/to/index_file")
        exit(1)

    # NOTE: You should already have used pyserini to generate the index files
    # before calling main
    index_fname = sys.argv[1]
    index_reader = IndexReader(index_fname)  # Reading the indexes

    # Print some basic stats
    print("Loaded dataset with the following statistics: " + str(index_reader.stats())) 

    print("Initializing PLN Ranker")
    pln_ranker = PivotedLengthNormalizatinRanker(index_reader)
    run_task(pln_ranker, 'covid', 10)

    print("Initializing BM25 Ranker")
    bm25_ranker = BM25Ranker(index_reader)
    run_task(bm25_ranker, 'gaming')
    
    print("Initializing Custom Ranker")
    custom_ranker = CustomRanker(index_reader)
    run_task(custom_ranker, 'android')
