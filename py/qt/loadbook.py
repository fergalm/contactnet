
import pandas as pd
import numpy as np 
from book import Book 

def load_book(fn):
 
    df = pd.read_csv(fn)
    df['idnum'] = df['idnum'].replace(np.nan, -1).astype(int)
    df['id1'] = df['id1'].replace(np.nan, -1).astype(int)
    tags = df[['tag1', 'tag2', 'tag3', 'tag4']].replace(np.nan, "")
    df['tags'] = tags.agg(','.join, axis=1)    
    df = df.replace(np.nan, "")
    
    namedf = df[['idnum', 'Name', 'about', 'tags']]
    reldf = df[['idnum', 'R1', 'id1']]
    reldf = reldf[ reldf.id1 > 0]
    reldf = reldf.rename( {'idnum': 'id1', 'R1':'connection', 'id1':'id2'}, axis=1)
    book = Book(namedf, reldf)
    #print(namedf)
    return book
