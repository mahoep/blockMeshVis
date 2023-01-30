# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 15:22:05 2023

@author: Matt
"""

import numpy as np


class Block:
    """
    Class definition for a Block.
    Holds information that describe the blocks vertexNum in space. How they 
    connect and the edge behavior
    """
    
    def __init__(self, kind='hex'):
        self.kind = kind
        if self.kind == 'hex':
            self.vertexNum = np.empty((8,),dtype=int)
            self.vertexVal = np.empty((8,3),dtype=float)
            self.edges = np.empty((12,2), dtype=int)
            self.xCells = int()
            self.yCells = int()
            self.zcells = int()
            
        elif self.kind == 'wedge':
            # self.vertexNum == np.zeros(6)
            raise NotImplementedError("Block does not support wedges at this time.")
        
            
    def assignNum(self, vertexNum):
        self.vertexNum = np.copy(vertexNum)
        self.p0 = self.vertexNum[0]
        self.p1 = self.vertexNum[1]
        self.p2 = self.vertexNum[2]
        self.p3 = self.vertexNum[3]
        self.p4 = self.vertexNum[4]
        self.p5 = self.vertexNum[5]
        self.p6 = self.vertexNum[6]
        self.p7 = self.vertexNum[7]
        
        #edges of the block. written from -> to
        self.edges[0]  = np.array([self.p0, self.p1])
        self.edges[1]  = np.array([self.p3, self.p2])
        self.edges[2]  = np.array([self.p7, self.p6])
        self.edges[3]  = np.array([self.p4, self.p5])
        self.edges[4]  = np.array([self.p0, self.p3])
        self.edges[5]  = np.array([self.p1, self.p2])
        self.edges[6]  = np.array([self.p5, self.p6])
        self.edges[7]  = np.array([self.p4, self.p7])
        self.edges[8]  = np.array([self.p0, self.p4])
        self.edges[9]  = np.array([self.p1, self.p5])
        self.edges[10] = np.array([self.p2, self.p6])
        self.edges[11] = np.array([self.p3, self.p7])
    
    def assignVal(self, vertexValList):
        for i in range(0,8):
            self.vertexVal[i,:] = np.copy(vertexValList[self.vertexNum[i]])
            
        
        
        
if __name__ == "__main__":
    blocks = Block()
