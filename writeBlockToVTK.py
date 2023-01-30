# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:38:00 2023

@author: Matt
"""

import vtk
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkLine)


def writeBlock(vertexValList, blocks):
    
    N = len(vertexValList)
    points = vtkPoints()

    for i in range(N):
        points.InsertNextPoint( list(vertexValList[i,:]))
    
    lines = vtkCellArray()
    
    for j in range(len(blocks)):
        line = vtkLine()
        #vtkLine has two ids, representing the two points that define a line.
        # the first number in SetId() is the Id relative to the line. The second
        # number is the id for the point we want from the vtkPoints() list
        # (I guess the c++ bindings abstract some things away here)
        for i in range(len(blocks[j].edges)):
            line.GetPointIds().SetId(0, blocks[j].edges[i,0])
            line.GetPointIds().SetId(1, blocks[j].edges[i,1])
            lines.InsertNextCell(line)

    # Create a polydata to store everything in
    polyData = vtkPolyData()

    # Add the points to the dataset
    polyData.SetPoints(points)

    # Add the lines to the dataset
    polyData.SetLines(lines)
    
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName("Block.vtk")
    writer.SetInputData(polyData)
    writer.Update()
    writer.Write()

if __name__ == '__main__':
    from parseBlockMeshDict import *
    with open('blockMeshDict','r') as file:
        blockMesh = file.readlines()
        
    a = find_sub_dict('vertices', blockMesh)
    vertexValList = convert_vertices_sub_dict(a)
    
    c = find_sub_dict('blocks', blockMesh)
    blocks = convert_blocks_sub_dict(c, vertexValList)
    
    writeBlock(vertexValList, blocks)