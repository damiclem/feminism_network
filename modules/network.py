# Dependencies
import numpy as np
import pandas as pd
import networkx as nx


# Define function for getting word map to integer
def map_words(words):
    # Get unique lemmas
    unique_words = words.groupby(by=['text', 'pos']).size().reset_index(name='counts')
    unique_words.sort_values(by='counts', ascending=False, inplace=True)
    # Map each unique lemma to a number and vice versa
    w2i, i2w = dict(), dict()
    for index, word in unique_words.iterrows():
        w2i.setdefault((word.text, word.pos), index)
        i2w.setdefault(index, (word.text, word.pos))
    # Return dictionaries
    return w2i, i2w

# Define function for creating edges dataset
def get_edges(words):
    """
    Input:
    - words dataset containing words (nodes)
    Output
    - edges: word edges DataFrame (node_x, node_y, counts)
    """
    
    # Make join to obtain words in the same tweet
    edges = pd.merge(words, words, on='tweet')
    edges = edges[edges.index_x != edges.index_y]  # Remove self join

    # Count how many times the same word matches have been found
    edges = edges.groupby(['node_x', 'node_y']).size()
    edges = edges.reset_index(name='counts')

    # Return edges dataset
    return edges

# Define function for saving edges to disk
def save_edges(edges_path, vocab_path, edges, w2i, i2w):
    # Save edges Pandas Dataframe object as csv
    edges.to_csv(edges_path, index=False)
    # Save edges vocabulary as numpy object
    np.save(file=vocab_path, arr={
        'w2i': w2i,
        'i2w': i2w
    })


# Define function for loading edges from disk
def load_edges(edges_path, vocab_path):
    # Load Pandas DataFrame object from disk
    edges = pd.read_csv(edges_path)
    # Load vocabularies
    vocab = np.load(vocab_path, allow_pickle=True).item()
    w2i = vocab['w2i']
    i2w = vocab['i2w']
    # Return either edges and vocabularies
    return edges, w2i, i2w

# Define function to retrieving degree as Pandas Series object
def get_degree(network):
    return pd.Series({node: degree for node, degree in nx.degree(network, weight='counts')})