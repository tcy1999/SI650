import os
import pandas as pd
import numpy as np
import json
# from pyserini.search import SimpleSearcher


def convertQuery(folder, filename):
    df = pd.read_csv(folder + '/' + filename)
    df = df.dropna(subset=['Query Description'])
    out = []

    for index, row in df.iterrows():
        temp_dict = {}
        temp_dict['id'] = row['QueryId']
        temp_dict['contents'] = row['Query Description']
        out.append(temp_dict)
    
    with open(folder + '/query/query.json', 'w') as file:
        json.dump(out, file)


def convertDoc(folder, filename):
    df = pd.read_csv(folder + '/' + filename)
    df = df.fillna('')
    out = []
    title = 'Document Title'
    if folder == 'covid':
        title = 'Title'

    for index, row in df.iterrows():
        temp_dict = {}
        temp_dict['id'] = row['DocumentId']
        temp_dict['contents'] = row[title] + ' ' + row['Document Description']
        if temp_dict['contents'] is not '':
            out.append(temp_dict)
    
    with open(folder + '/doc/doc.json', 'w') as file:
        json.dump(out, file)

""" 
def testing():
    searcher = SimpleSearcher('android/indexes)
    hits = searcher.search('document')

    for i in range(len(hits)):
        print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
 """

if __name__ == '__main__':
    convertDoc('android', 'documents_android.csv')
    convertDoc('covid', 'documents.csv')
    convertDoc('gaming', 'documents_gaming.csv')
    convertQuery('android', 'query_android.csv')
    convertQuery('covid', 'query.csv')
    convertQuery('gaming', 'query_gaming.csv')
    # testing()
