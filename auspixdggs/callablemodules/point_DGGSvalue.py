# -*- coding: utf-8 -*-
"""
Created on 1st March 2019

@author: Joseph Bell Geoscience Australia
"""

'''
small module to find the DGGS cell for a point (long, lat) WGS84
'''
from ..auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS()

def latlong_to_DGGS(coords, resolution):

    # calculate the dggs cell from long and lat
    thisCell = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve

    # now have a dggs cell for that point
    print('DGGScell', thisCell)
    return thisCell

if __name__ == '__main__':
    coordinates = (148.9668333, -35.38275)
    print('test values', coordinates)
    answer = latlong_to_DGGS(coordinates, 12)  #12 is the resolution

    print('answer', answer)
    print('finished')
