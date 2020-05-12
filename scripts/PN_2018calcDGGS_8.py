# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph
"""

'''
reads a csv file and adds DGGS to it

This is for placeNames 
Placenames is from 2018 
Rob Kay supplied the csv
Code fields were converted into their full text equivalent while building the query

'''


f = r'\\xxxxxxxxxxxxxxxxxx\PLACENAMES_2018.csv'

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
myHeader = "ID, Name, DGGSrHealpix, Longi, Lati"
myPoints.append(myHeader)
# open the data file 
with open(f) as csvDataFile:
    csvReader = csv.reader(csvDataFile)

    next(csvReader)  # skip the header
    output.append('_ID, AUTH_ID, NAME, FEATURE, CATEGORY, GROUP, LATITUDE, LONGITUDE, '
                  'AUTHORITY, SUPPLY_DATE, DGGSrHealpix, Point_conf_±_m, DGGS_level')
    for row in csvReader:
        
        #read in the latlong
        longi = float(row[7])
        lati = float(row[6])
                
        # feed lat long into convertor
        
        #Pick a (longitude-latitude) point on the ellipsoid and find the resolution 1 cell that contains it ::
        t = (longi, lati)
        resolution = 12  # set the resolution

        plane = False  # on curve

        w = rdggs.cell_width(resolution)
        if plane:
            area = w**2
        else:
            area =8/(3* math.pi)*w**2
        
        #calculate the ± error
        errored = (math.sqrt(area))/2
        # change to metres with one decimal place
        conf = (" %2.1f m" % (errored))
        # print ()

        # calculate the dggs cell from long and lat ie t
        thisCell = rdggs.cell_from_point(resolution, t, plane=False)  # false = on the curve
        #dggsCell = str(thisCell)

        # #find the boundary
        # dggsLoc = list()
        # for item in dggsCell:   # build a dggs location cell as a list like dggsLoc = ['R', 7, 2, 4, 5, 6, 3, 2, 3, 4, 3, 8, 3]
        #     if item.isalpha():
        #         dggsLoc.append(item)
        #     else:
        #         item = int(item)
        #         dggsLoc.append(item)

        #print (dggsLoc)


        # c = rdggs.cell(dggsCell)
        # print (c)


        try:

            #build output
            pushout = (str(row[0])+','+ str(row[1])+ ','+ str(row[2])+ ','+ str(row[3])+
                       ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7])+
                       ',' + str(row[8]) + ',' + str(row[9]) + ',' + str(thisCell) + ',' + conf +
                      ',' + str(resolution) )

            output.append(pushout)
        except:
            print('failed', str(row[0]), p, c)  # fails on Tasmanian where changes from R to S
            failed += 1
            pass



# Build the ttl
# write the file
#filename = 
# overwrites previous file unless you rename or move it
write_list_to_file(output, r"\\xxxxxxxx\DGGS_py\PlacesNames2018with_12_DGGS.csv")




print ('number failed = ', failed)
#
#for row in output:
#
#    print(row)
#    
print ("finished")
    
    