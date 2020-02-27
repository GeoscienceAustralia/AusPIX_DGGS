# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph Bell Geoscience Australia
"""

'''
reads a csv file and adds DGGS to it

This is for river gauges data csv from BoM 30 Nov 2018
Placenames is from 2018 

The code finds the DGGS cell for each location (level 12?)

'''


f = r'\\xxxxxxx\RiverGauges\RiverGaugeLocationsAU.csv'

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
myHeader = "Name, Station, DataOwner, DGGSrHealpix, Longi, Lati"
myPoints.append(myHeader)
# open the data file 
with open(f) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    next(csvReader)  # skip the header
    output.append('Name, Station_No, Name, Latitude, Longitude, DGGSrHealpic, CellWidth, DggsLevel, NW, NE, SE, SW')

    for row in csvReader: # read through the source file line by line
        if not str(row[2]).startswith('xxx'):  # filter to get ACT
            # print(row)
            # read in the latlong
            longi = float(row[4])
            lati = float(row[3])

            # feed lat long into convertor

            #Pick a (longitude-latitude) point on the ellipsoid and find the cell that contains it ::
            t = (longi, lati)

            #figure resolution to use using longitude
            strLongi = str(longi)  # convert longi to string
            strLati = str(lati)

            resolution = 10
            plane = False  # on curve

            w = rdggs.cell_width(resolution)
            if plane:
                area = w**2
            else:
                area =8/(3* math.pi)*w**2


            # change to metres with one decimal place
            w = (" %2.0f m" % (w))
            # print ()

            # calculate the dggs cell from long and lat ie t
            thisCell = rdggs.cell_from_point(resolution, t, plane=False)  # false = on the curve
            dggsCell = str(thisCell)

            #find the boundary for exporting into ESRI or GDAL
            dggsLoc = list()  # empty list ready to fill
            for item in dggsCell:   # build a dggs location cell as a list like dggsLoc = ['R', 7, 2, 4, 5, 6, 3, 2, 3, 4, 3, 8, 3]
                if item.isalpha():  # the letter 'R' at the beginning
                    dggsLoc.append(item)
                else:
                    item = int(item)   # the numbers in the cell
                    dggsLoc.append(item)

            c = rdggs.cell(dggsLoc)
            # print (c)
            bound = list()
            # put in try statement for Tasmanian ones that produce an error?
            try:
                for p in c.boundary(n=2, plane=False):
                    bound.append(p)
                    #prepare for shapefile output
                    myPoints.append(str(row[0])+ ', ' + str(row[1] + ',' + str(row[2]) + ',' + str(thisCell) + ',' + str(p[0]) + ', ' + str(p[1])))

                NW = cleanPosition(str(bound[0]))
                NE = cleanPosition(str(bound[1]))
                SE = cleanPosition(str(bound[2]))
                SW = cleanPosition(str(bound[3]))
                #print(bound)
                #print()

                #build output
                pushout = (str(row[0])+','+ str(row[1])+ ','+ str(row[2])+ ','+ str(row[3])+ ',' + str(row[4]) + ','  +
                           str(thisCell) + ',' + w + ',' + str(resolution) + ',' + str(NW) + ',' + str(NE) + ',' + str(SE) + ',' + str(SW))

                output.append(pushout)
            except:
                print('failed', str(row[0]), p, c)
                failed += 1   # count the errors
                pass



# output the data to csv files
# overwrites previous file unless you rename or move it
write_list_to_file(output, r'\\xxxxxxx\RiverGauges\RiverGaugeLocationsAU_DGGS10.csv')
#
write_list_to_file(myPoints, r'\\xxxxxx\RiverGauges\RiverGaugeLocationsAU_points10.csv')


print ('number failed = ', failed)
#
#for row in output:
#
#    print(row)
#    
print ("finished")

