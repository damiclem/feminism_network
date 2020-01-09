import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

''' 
Takes in input the year of interest (string), returns a dataframe of words 
extracted from tweets from that year.
'''

def select_year(year):
    # Retrieve words from database .csv tables
    words = pd.read_csv('data/database/words.csv', dtype={
        'tweet': np.unicode_,
        'index': np.int,
        'text': np.unicode_,
        'pos': np.unicode_,
        'conf': np.float
    })
    # Load tweets data
    tweets = pd.read_csv('data/database/tweets.csv')[['created_at','id_str']]
    
    # Filter tweets 
    mask = [ x[-4:] == year for x in tweets.created_at.values  ]
    tweets_y = list(tweets.loc[mask,'id_str'].astype('str').values)
    
    # Filter words from 2017 tweets
    words17 = words.loc[words.tweet.isin(tweets_y),:]
    
    return words17

'''
Takes in input the dataframe of words, returns:
- w2i dictionary that maps words to a unique integer index;
- edges dataframe with index and text for each word belonging to an edge of the graph.
'''

def create_edges(words):
    # Define edges: words with a common tweet
    edges = pd.merge(words, words, on='tweet')
    edges = edges[edges.index_x != edges.index_y]  # Remove self join

    # Count how many times the same word matches have been found
    edges = edges.groupby(['text_x', 'text_y']).size().reset_index(name='counts')
    
    # Map each unique concept to a number and vice versa 
    w2i, i2w = dict(), dict()
    for index, word in enumerate(set(words.text)):
        w2i[word] = index
        i2w[index] = word
    
    # Map each word to a numeric index
    edges['number_x'] = edges.text_x.map(w2i)
    edges['number_y'] = edges.text_y.map(w2i)
    edges.head()
    
    return w2i, edges

'''
Takes in input the w2i dict and the edge dataframe, returns the corresponding adjacency matrix A.
'''

def adj_matrix(w2i, edges):
    # Define number of unique words available
    n = len(w2i.keys())

    # Initialize adjacency matrix
    A = np.zeros(shape=(n, n), dtype=np.int)

    # Loop through each edge to fill adjacency matrix
    for i, edge in edges.iterrows():
        # Fill each cell with counts 
        A[edge.number_y][edge.number_x] = edge.counts
        
    return A

'''
Takes in input the values assumed by the degree distribution (unique), the pdf and the cpdf of degrees. Returns the pdf linear plot,
the  pdf loglog plot and the cpdf loglog plot.
'''

def plots(k,pdf,cpdf):
    fig, ax = plt.subplots(1,2,figsize=(15,8))
    ax = ax.ravel()

    ax[0].plot(k, pdf,'o')
    ax[0].set_title('linear PDF')
    ax[0].grid()

    ax[1].loglog(k, pdf,'o')
    ax[1].set_title('loglog PDF')
    ax[1].grid()
    
    fig, ax = plt.subplots(1,1,figsize=(15,8))
    ax.loglog(k, cpdf,'o')
    ax.set_title('loglog CPDF')
    ax.grid()
    
    plt.show()