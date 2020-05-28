# -*- coding: utf-8 -*-
"""
Created on Feb 2019

@author: Joseph Bell Geoscience Australia
"""


# -*- coding: utf-8 -*-

'''
This code recieves a rHealpix cell and compares it to another data set eg SA1
to return the polygon it's centroid is inside

Joseph Bell Geoscience Australia

'''
from ..auspixengine.dggs import RHEALPixDGGS
from ..auspixengine.dggs import Cell
import shapefile
import os

from . import call_DGGS  # returns the DGGS cells for a shapefile poly
# or use dggs_in_poly.py module

from shapely.geometry import shape, Point, Polygon  # used in the function below

import csv

# make an dggs instance
rdggs = RHEALPixDGGS()
''' function to tell which polygon of a shapefile a DGGS cell is in '''
def get_matching_polygon( rHealpix_cell, shapeFile_path):
    # read in the file
    r = shapefile.Reader(shapeFile_path)
    fields = r.fields[1:]
    # for item in r.fields:
    #     print(item)  # prints the fields in the shapefile??

    # get the attribute table records (combined with shapes) ie shapeRecords
    shapeRecs = r.shapeRecords()

    print(rHealpix_cell)

    #find centroid
    # make an dggs instance
    rdggs = RHEALPixDGGS()

    thisDGGS = rHealpix_cell
    # print(thisDGGS)
    # print(' ')
    # convert to proper format
    dggsLoc = list()  # empty list ready to fill
    for item in thisDGGS:  # build a dggs location cell as a list like dggsLoc = ['R', 7, 2, 4, 5, 6, 3, 2, 3, 4, 3, 8, 3]
        if item.isalpha():  # the letter 'R' at the beginning
            dggsLoc.append(item)
        else:
            item = int(item)  # the numbers in the cell
            dggsLoc.append(item)

    c = Cell(rdggs, dggsLoc)
    centroid = c.centroid(plane=False)
    nucleus = c.nucleus()  #seems to be in meters

    print('nucleus', nucleus[0], nucleus[1])  #nucleus seems to be in metres - need it in Lat Long
    print('centroid', centroid[0], centroid[1])
    dggsPoint = Point(centroid[0], centroid[1])

    #findout which poly the centroid is in
    # use shapely

    #for spatial shape in shapefile
    for item in shapeRecs:
        thisItem = item.shape
        # define the shape and give it to shapely
        thisShp = thisItem.points  # this gives a list of points the function input poly has in it
        # now convert to a shapely Polygon
        thisPoly = Polygon(thisShp)  # thisPoly is the Shapely version of the poly

        if dggsPoint.within(thisPoly):  # take the point from DGGS cell nucleus
            print('Found SA1', item.record[0])
            return item.record[0]


if __name__ == '__main__':
    # main
    #SA1
    myFile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data', 'ACT_SA1', 'SA1_ACT_2016.shp')
    print('test file: {}'.format(myFile))

    # try with SA2
    #myFile = r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\Meshblocks\1270055001_sa2_2016_aust_shape\SA2_2016_AUST.shp'

    answer = get_matching_polygon('R7852608578', myFile)
    print(repr(answer))
    print('answer SA1 =', answer[1])

    print('finished')
