# -*- coding: utf-8 -*-
"""
Created on 1st March 2019

@author: Joseph Bell Geoscience Australia
"""

'''
small module to find the DGGS cell for a point (long, lat) WGS84
The point will be anywhere in the cell returned.

'''
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS()

def latlong_to_DGGS(coords, resolution):

    # calculate the dggs cell from long and lat
    thisCell = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve

    # now have a dggs cell for that point
    print('DGGScell', thisCell)
    return thisCell

if __name__ == '__main__':
    coordinates = (148.9668333, -35.38275)
    print('test coords', coordinates)
    answer = latlong_to_DGGS(coordinates, 10)  #10 is the resolution cell area = 2.4408 ha

    print('answer', answer)
    print('finished')
