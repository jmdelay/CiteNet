#!/usr/bin/env python3
"""
Created on Sun Feb  6 17:56:19 2022

@author: J. Mac DeLay; University of Alabama at Birmingham
    
Pilot citation network mining for article impact analysis.

Article: 
Hampson, Joan G., John William Money and John L. Hampson.
“Hermaphrodism: recommendations concerning case management.”
The Journal of clinical endocrinology and metabolism 16 4 (1956): 547-56.
DOI:10.1210/JCEM-16-4-547
Corpus ID: 21487842
"""

import json
import networkx as nw
import numpy as np
from semanticscholar import SemanticScholar
import matplotlib.pyplot as plt

sch = SemanticScholar(timeout=200)

def initG(DOI: str) -> dict:
    """take the DOI from the seed article and produce a labelbase for each
    descendant
    
    Params:
        DOI: (str) Semantic Scholar DOI for seed article
    Returns:
        (dict) articles collected and their labels
        FORMAT::
            Source CitedBy CitedBy CitedBy . . .
            .
            .
            .
    """
    
    paper = sch.paper(DOI)
    cites = paper['citations']
    
    
    G = nw.DiGraph()
    #tabDOI = open('DOItab.txt','w')
    for child in range(len(cites)):
        v = cites[child]['doi']
            
        if v != None:
            #tabDOI.write(v + '\n')
            G.add_edge('10.1210/JCEM-16-4-547', v)
                
    # for each child, get citation list and add its children, repeat
    
    #tabDOI.close()
    
    return G



def explode(G: nw.DiGraph) -> nw.DiGraph:
    """describe
    
    Params:
        
    Returns:
        
    """
    with open('DOItab.txt','w') as tab:
        nodeList = list(nw.nodes(G))
    
        for v in range(len(nodeList)):
            
            current = nodeList[v]
            print(current)
            
            try:
                paper = sch.paper(current)
            except PermissionError:
                tab.write('Article '+current+' omitted due to permsission error. \n')
                continue
            cites = paper['citations']
           
            for child in range(len(cites)):
                leaf = cites[child]['doi']
                    
                if leaf != None:
                    tab.write(leaf + '\n')
                    G.add_edge(current, leaf)
                    
                            
        # for each child, get citation list and add its children, repeat
        
    return G


def main():
    #G = initG('10.1210/JCEM-16-4-547')
    #G = explode(G)
    G=nw.read_edgelist("G.edges.gz",create_using=nw.DiGraph())
    G = explode(G)
    nw.write_edgelist(G, "G.edges.gz")
    return 0

#main()

G=nw.read_edgelist("G.edges.gz",create_using=nw.DiGraph())
outList = []
nodes = list(G.nodes())
for v in nodes:
    outList.append(G.out_degree(v))
    
outList = np.asanyarray(outList)
nw.draw(G)
plt.show()
plt.hist(outList[outList>0],bins=50)
plt.title('Distr of OutDegree')
plt.show()

''' JSON DUMP
with open('labelsExample.txt', 'w') as file:
     file.write(json.dumps(paper))
'''
