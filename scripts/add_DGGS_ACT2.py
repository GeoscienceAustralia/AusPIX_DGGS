# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph Bell Geoscience Australia
"""

'''
reads a csv file and adds DGGS to it

This is for placeNames 
Placenames is from 2018 
A query was used to gather basic placename data into a csv
Code fields were converted into their full text equivalent while building the query

This code reflects the number of decimal points in the lat and long by adjusting the size of the DGGS box.
In practice the DGGS boxes were often too big. Needs adjusting eg a level DGGS 5 box is too big for anything. 

'''

f = r'\\xxxxxxxx\ACT_grid\ACT_Points.csv'

output = list()

import csv
from auspixdggs.auspixengine.dggs import RHEALPixDGGS

import math
from auspixdggs.auspixengine.utils import my_round

# make an instance
rdggs = RHEALPixDGGS()


# function to write a list to a csv file
# requires the list and the filename to save it too
def write_list_to_file(myList, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in myList:
            outfile.write(entries)
            # add a return after each line
            outfile.write("\n")


def cleanPosition(pos):
    pos = pos.replace('(', '')
    pos = pos.replace(')', '')
    pos = pos.replace(',', ' ')
    return pos


failed = 0
myPoints = list()
myCells = list()
myHeader = "ID, Name, DGGSrHealpix, Longi, Lati"
myPoints.append(myHeader)
# open the data file
with open(f) as csvDataFile:
    csvReader = csv.reader(csvDataFile)

    next(csvReader)  # skip the header

    for row in csvReader:
        # read in the latlong
        longi = float(row[2])
        lati = float(row[3])

        # feed lat long into convertor

        # Pick a (longitude-latitude) point on the ellipsoid and find the resolution cell that contains it ::
        t = (longi, lati)


        # set the resolution
        resolution = 10
        # calculate the dggs cell from long and lat ie t
        thisCell = rdggs.cell_from_point(resolution, t, plane=False)  # false = on the curve
        # now have a dggs cell for that point

        if thisCell not in myCells:  # filter out cells already in there - only do the new ones
            myCells.append(thisCell)
            dggsCell = str(thisCell)
            # find the boundary
            dggsLoc = list()
            for item in dggsCell:  # build a dggs location cell as a list like dggsLoc = ['R', 7, 2, 4, 5, 6, 3, 2, 3, 4, 3, 8, 3]
                if item.isalpha():
                    dggsLoc.append(item)
                else:
                    item = int(item)
                    dggsLoc.append(item)
            #print()
            # print(dggsLoc)

            c = rdggs.cell(dggsLoc)
            # print (c)
            bound = list() # a list for the cell boundary

        #try:
            for p in c.boundary(n=2, plane=False):
                bound.append(p)
                # prepare for shapefile output

                #print(str(row[0]))
                myPoints.append(
                    str(row[0]) + ', ' + str(row[1]) + ',' + str(thisCell) + ',' + str(p[0]) + ', ' + str(p[1]))


            print (str(row[0]) + ', ' + str(row[1]) + ',' + str(thisCell) + ',' + str(p[0]) + ', ' + str(p[1]))

            # NW = cleanPosition(str(bound[0]))
            # #print ('NW = ', NW)
            # NE = cleanPosition(str(bound[1]))
            # SE = cleanPosition(str(bound[2]))
            # SW = cleanPosition(str(bound[3]))
            # # print(bound)
            # # print()
            #
            # # build output
            # pushout = (str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) +
            #            ',' + str(resolution) + ',' + str(NW) + ',' + str(NE) + ',' + str(SE) + ',' + str(SW))
            # #print (pushout)
            # output.append(pushout)
        #except:
            # print('failed', str(row[0]), p, c)
            # failed += 1
            # pass


# overwrites previous file unless you rename or move it
# write_list_to_file(output, r"\\xxxxxx\ACT_grid\ACT_Grid_bounds.csv")
#
write_list_to_file(myPoints, r"\\xxxxxxx\temp\PN_boundings.csv")


print('number failed = ', failed)
#
# for row in output:
#
#    print(row)
#
print("finished")

