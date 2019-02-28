# -*- coding: utf-8 -*-
"""
Created on 1st March 2019

@author: Joseph Bell Geoscience Australia
"""

'''
small module to find the DGGS cell for a point (long, lat) 

'''
from dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS()

def latlong_to_DGGS(coords, resolution):

    # Pick a (longitude-latitude) point on the ellipsoid and find the resolution cell that contains it ::
    # coords = (longi, lati)  # format required like this

    # set the resolution
    #resolution = 10
    # calculate the dggs cell from long and lat ie t
    thisCell = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve

    # now have a dggs cell for that point
    print('DGGScell', thisCell)
    return thisCell



if __name__ == '__main__':
    # main
    #SA1
    coordinates = (148.9668333, -35.38275)
    print('test values', coordinates)
    answer = latlong_to_DGGS(coordinates, 12)

    print('answer', answer)

    print('finished')