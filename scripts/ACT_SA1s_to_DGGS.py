# -*- coding: utf-8 -*-
"""
Created on Feb 2019

@author: Joseph Bell Geoscience Australia
"""


# -*- coding: utf-8 -*-

'''
This code calculates all the rHealPix cells in a polygon at the resolution asked for.
It will calculate the DGGS cells and return them to the code.
This example is based on ABS SA1
ESRI not required but python module shapefile is.

Joseph Bell Geoscience Australia

'''


from auspixdggs.auspixengine.dggs import RHEALPixDGGS
from auspixdggs.auspixengine.dggs import Cell
import auspixdggs.callablemodules.call_DGGS as call_DGGS
import shapefile

import auspixdggs.callablemodules.call_DGGS  # returns the DGGS cells for a shapefile poly

from shapely.geometry import shape, Point, Polygon  # used in the function below
import csv



#set up shapefile for output
w = shapefile.Writer(shapefile.POINT)

w.field('DGGSrHEALPix', 'C', '20')
w.field('LongiWGS84', 'C', '20')  #using 'C' = character = ensures the correct number
w.field('LatiWGS84', 'C', '20')
w.field('Approx_width', 'C', '20')
w.field('DGGS_reso', 'C', '20')
w.field('LGAcode', 'C', '20')
w.field('Name', 'C', '20')
w.field('dggs_cell', 'C', '100')

# make an dggs instance
rdggs = RHEALPixDGGS()


# open a shape file to get your polygons from
#myFile = r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\Meshblocks\1270055001_sa1_2016_aust_shape\SA1_2016_AUST.shp'
#myFile = r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\LGA\SA1_ACT_2016.shp'
myFile = '../test_data/ACT_SA1/SA1_ACT_2016.shp'

#SA1's can be downloaded from ABS?

# read in the file
r = shapefile.Reader(myFile)

# get the attribute table records (combined with shapes) ie shapeRecords
shapeRecs = r.shapeRecords()
#
#
# function to write a list to a csv file
# requires the list and the filename to save it too
def write_list_to_file(myList, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in myList:
            outfile.write(entries)
            # add a return after each line
            outfile.write("\n")
#
#
# # set the resolution between about 2 to 12 - bigger numbers mean smaller cells
# # resolution = 9


csvOutput = list()  # initialise
dataList = list()
dataList.append(('SA1code', 'SA2name16', 'Areakmsq', 'Num_cells', 'DGGS'))
for feature in shapeRecs: # slice of x polygons from the whole shapefile [0:20]
    newRow = list()

    # filter out the ACT SA1's
    if feature.record[8] == 'Australian Capital Territory':
        # in ACT
        print(feature.record[0], feature.record[4], feature.record[13])

#     thisRecord = feature.record[0:] # the attribute table record
#     print('len of record', len(thisRecord))
#     print(thisRecord)
#     print('found LGA called ', thisRecord[2])
#
        polyShape = feature.shape  # get the spatial component
        polyRecord = feature.record  # get the attributes record (row)
        area = float(feature.record[13])  # needs to point to the area of the polygon in the data sqkm
        print('Area', area)
        print(type(area))
#
#
        resolution = 10  # default resolution
        # vary resolution based on area so bigger areas have bigger cells

        # if area < 1:
        #     resolution = 12
        # elif area > 1 and area < 1000.0:
        #     resolution = 9
        # elif area > 1000.0 and area < 30000.0:
        #     resolution = 6
        # elif area > 30000:
        #     resolution = 4

        print('using resolution ', resolution)
        # calculate the approx cell width at this resolution
        thisWidthApprox = rdggs.cell_width(resolution,
                                           plane=True)  # note only approx because we are using the planar to estimate elipsoidal
        print('++++++++++ Cell width approx  +++', thisWidthApprox, 'm')
        thisSA1 = feature.record[0]
        thisName = feature.record[2]
#
        # call the "call_DGGS" function to return all the DGGS cells (within polygon only)
        cells_in_poly = call_DGGS.poly_to_DGGS_tool(polyShape, polyRecord, resolution)
        print('number in polygon = ', len(cells_in_poly))
#
#         print ('Reducing . . . ')
#         # reduce to biggest cells
#         theseReducedCells = call_DGGS.coalesce(cells_in_poly)
#         #print('reduced cells =', theseReducedCells)
#         print('1st number reduced cells =', len(theseReducedCells))
#
#         # reduce again
#         theseReducedCells = call_DGGS.coalesce(theseReducedCells)
#         #print('2nd reduced cells =', theseReducedCells)
#         print('2nd number reduced cells =', len(theseReducedCells))
# #
#     # reduce again
#     theseReducedCells = call_DGGS.coalesce(theseReducedCells)
#     # print('3nd reduced cells =', theseReducedCells)
#     print('3nd number reduced cells =', len(theseReducedCells))
#
#     # reduce again
#     theseReducedCells = call_DGGS.coalesce(theseReducedCells)
#     # print('3nd reduced cells =', theseReducedCells)
#     print('4nd number reduced cells =', len(theseReducedCells))
#
#     # # reduce again
#     # theseReducedCells = call_DGGS.coalesce(theseReducedCells)
#     # # print('3nd reduced cells =', theseReducedCells)
#     # print('5nd number reduced cells =', len(theseReducedCells))
#

        #newRow.append((feature.record[0], feature.record[4], feature.record[13], len(theseReducedCells), theseReducedCells))
        dataList.append((feature.record[0], feature.record[4], feature.record[13], len(cells_in_poly), cells_in_poly))
print()
print()
for item in dataList:
    print(item)

for item in dataList:
    if 'R7852335255' in item[4]:
        print('found R7852335255')
        print(item)

