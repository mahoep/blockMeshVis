# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 12:42:57 2023

@author: Matt
"""

import re
import numpy as np

from blockMesh import Block


def find_sub_dict(subDictName, blockMeshDict):
    """
    Parameters
    ----------
    subDictName : string
        name of the dictionary that is to be parsed.
    blockMeshDict : list of strings
        contains each line of text from blockMeshDict.

    Raises
    ------
    RuntimeError
        If the dictionary can not be found or parsed.

    Returns
    -------
    list of strings
        contains each line of text from the sub dictionary of choice.
    """
    
    allSubDictEnds = np.array([])
    for n in range(len(blockMeshDict)):
        
        line = blockMeshDict[n].strip('\n')
        
        if len(line) != 0:
            if (subDictName in line) and ('//' not in line.strip()[0:2]):
                # only parse if the line is not empty, the name is in the line, and
                # there are not c/c++ style comments in front
                subDictStart = n
        # find all locations where semi-colons exsist. They mark the end of each sub dictionary
        if ';' in line:
            allSubDictEnds = np.append(allSubDictEnds, n)
            
    # the end of a sub dictionary is equal to the minimum positive line number distance from 
    # the sub dictionary name. i.e. from line 18-36 in rhoCentralFoam tutorial is vertices
    arr = allSubDictEnds - subDictStart
    subDictEnd = np.where(arr > 0, arr, np.inf).min() + subDictStart

    if subDictStart > 0 and subDictEnd > 0:    
        return blockMeshDict[int(subDictStart): int(subDictEnd)+1]
    else:
        raise RuntimeError("Sub dictionary entry in BlockMeshDict not found. Make sure \
    the line is uncommented (//) and spelled correctly")
     
    
def convert_vertices_sub_dict(verticesSubDict):
    """
     Parameters
     ----------
     verticesSubDict : list of strings
     contains each line of text from the sub dictionary of choice.
    
     Returns
     -------
     vertices : numpy array
     and Nx3 numpy array containing the vertex entries from the dictionary 
    """
    
    vertices = []
    for n in range(2,len(verticesSubDict)-1):
        if '/' not in verticesSubDict[n]:
            entry = (verticesSubDict[n].strip().replace(' ',','))
            
            tmp = entry.strip('( )').split()[0].split(',')
            vertices.append([float(i) for i in tmp])
        else:
            commentStart = verticesSubDict[n].find('/')
            entry = (verticesSubDict[n][0:commentStart].strip().replace(' ',','))
            
            tmp = entry.strip('( )').split()[0].split(',')
            vertices.append([float(i) for i in tmp])
        
    return np.array(vertices)
    

def convert_blocks_sub_dict(blocksSubDict, vertexValList):
    """
    Parameters
    ----------
    blocksSubDict : list of strings
        contains each line of text from the sub dictionary of choice.
    vertexValList : numpy array
        a Nx3 array containg the x,y,z coordinates of all vertices 

    Returns
    -------
    blocks : list of Blocks()
        contains a list of blocks (class Block) with contains information for 
        verticies, edges, etc.
    """
    
    numBlocks = "".join(blocksSubDict).count('hex')
    blocks = []
    k=0
    for n in range(len(blocksSubDict)):
        if 'hex' in blocksSubDict[n]:
            blocks.append(Block())
            entry = (blocksSubDict[n].strip())
            
            j=0
            # fancy regex stuff. copied from Stack Overflow no idea how it works
            # isolates numbers between parentheses i.e. (0 1 2 3) (1 1 1)
            for segment in re.findall("[(][^)]*[)]", entry):
                expression = re.findall(r"[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", segment)
                if j == 0:
                    blocks[k].assignNum([int(i) for i in expression])
                    blocks[k].assignVal(vertexValList)
                if j == 1:
                    blocks[k].xCells = expression[0]
                    blocks[k].yCells = expression[1]
                    blocks[k].zCells = expression[2]
                j+=1
            k+=1
    if k != numBlocks:
        import warnings
        warnings.simplefilter('error', UserWarning)
        warnings.warn('More blocks were created than entries in blockMeshDict.', UserWarning)
    
    return blocks
    

if __name__ == "__main__":
    with open('blockMeshDict','r') as file:
        blockMesh = file.readlines()
        
    a = find_sub_dict('vertices', blockMesh)
    vertexValList = convert_vertices_sub_dict(a)
    
    c = find_sub_dict('blocks', blockMesh)
    blocks = convert_blocks_sub_dict(c, vertexValList)
    
    