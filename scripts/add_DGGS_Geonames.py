# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph Bell
"""

'''
reads a csv file and adds DGGS to it

This is for Geonames 
Paul Box CSIRO is said to have built this dataset
https://www.geonames.org

'''

f = r'\\\PlacenamesGeonames\Geonames.csv'

output = list()


import csv
from auspixdggs.auspixengine.dggs import RHEALPixDGGS

import math
from auspixdggs.auspixengine.utils import my_round

# make an instance        
rdggs = RHEALPixDGGS()


# function to write a list to a csv file
# requires the list and the filename to save it to.
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
myHeader = list()



# open the data file
with open(f) as csvDataFile:
    csvReader = csv.reader(csvDataFile)

    header = str(next(csvReader))  # read in the header


    header = header.replace('[', '')
    header = header.replace(']', '')
    header = header.replace("'", "")


    # take the header off the source file and put it on the output
    output.append(header)

    for row in csvReader: # read through the source file line by line
        if not str(row[0]).startswith('XXX'):  # not filtered
        
            #read in the latlong
            longi = float(row[5])
            lati = float(row[4])

            #Pick a (longitude-latitude) point on the ellipsoid and find the cell that contains it ::
            t = (longi, lati)
            resolution = 12

            plane = False  # on curve

            w = rdggs.cell_width(resolution)
            if plane:
                area = w**2
            else:
                area =8/(3* math.pi)*w**2

            # change to metres with one decimal place
            w = (" %2.0f m" % (w))

            # calculate the dggs cell from long and lat ie t
            thisCell = rdggs.cell_from_point(resolution, t, plane=False)  # false = on the curve
            #dggsCell = str(thisCell)

            pushout = (str(row[0])+','+ str(row[1])+ ','+ str(row[2])+ ','+ str(row[3])+
                       ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7])+
                       ',' + str(row[8]) + ',' + str(row[9]) + ',' + str(row[10]) + ',' + str(row[11])+ ',' +
                       str(thisCell) + ',' + w + ',' + str(resolution) + ',' + str(row[15]) + ',' + str(row[16]) + ',' + str(row[17])+ ',' + str(row[18]))

            output.append(pushout)



# output the data to csv files
# overwrites previous file unless you rename or move it
write_list_to_file(output, r"\\xxxxxxxxx\PlacenamesGeonames\Geonames_withDGGS.csv")




# for row in output:
#
#    print(row)
# #
print ("finished")





# # find the boundary for exporting into ESRI or GDAL
# dggsLoc = list()  # empty list ready to fill
# for item in dggsCell:  # build a dggs location cell as a list like dggsLoc = ['R', 7, 2, 4, 5, 6, 3, 2, 3, 4, 3, 8, 3]
#     if item.isalpha():  # the letter 'R' at the beginning
#         dggsLoc.append(item)
#     else:
#         item = int(item)  # the numbers in the cell
#         dggsLoc.append(item)
#
# # if resolution < 12:
# #     print (dggsLoc)

