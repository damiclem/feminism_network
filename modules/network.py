# Dependencies
import numpy as np
import pandas as pd
import networkx as nx

# Define function for creating edges dataset
def get_edges(words):
    """
    Input:
    - Dataset containing words (tweet, index, text, pos)
    Output
    - edges: word edges DataFrame (text_x, pos_x, text_y, pos_y, counts) 
    - w2i: dictionary mapping word (text, pos) to number
    - i2w: dictionary mapping number to word (text, pos)
    """
    
    # Make join to obtain words in the same tweet
    edges = pd.merge(words, words, on='tweet')
    edges = edges[edges.index_x != edges.index_y]  # Remove self join

    # Count how many times the same word matches have been found
    edges = edges.groupby(['text_x', 'pos_x', 'text_y', 'pos_y']).size()
    edges = edges.reset_index(name='counts')

    # Get unique word (text, POS) set
    unique_words = words.groupby(by=['text', 'pos']).size().reset_index(name='counts')
    # Map each unique concept to a number and vice versa 
    w2i, i2w = dict(), dict()
    for index, word in unique_words.iterrows():
        w2i[(word.text, word.pos)] = index
        i2w[index] = (word.text, word.pos)
    # Map each word to a numeric index
    edges['number_x'] = edges.apply(lambda e: w2i[(e.text_x, e.pos_x)], axis=1)
    edges['number_y'] = edges.apply(lambda e: w2i[(e.text_y, e.pos_y)], axis=1)

    # Return dataset
    return edges, w2i, i2w


# Define function for creating adjacency matrix
def get_adjacency(edges, n, triangular=False):
    """
    Input:
    - edges: DataFrame object containing edges between word nodes
    - n: the number of edges available
    - triangular: determines if the adjacency matrix should be made (upper) triangular
    Output:
    - X: numpy adjacency matrix 
    """
    
    # Initialize adjacency matrix
    X = np.zeros(shape=(n, n), dtype=np.int)
    
    # Loop through each edge to fill adjacency matrix
    for i, edge in edges.iterrows():
        # Handle trianguarization
        if triangular and edge.number_y > edge.number_x:
            continue
        # Fill each cell with counts
        X[edge.number_y][edge.number_x] = edge.counts
            
    # Return filled adjacency matrix
    return X