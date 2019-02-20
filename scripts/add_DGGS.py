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

f = r'\\xxxxxxPlaceNames_2018\PLACENAMES_2018.csv'

output = list()


import csv
from dggs import RHEALPixDGGS

import math
from utils import my_round

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
                  'AUTHORITY, SUPPLY_DATE, DGGSrHealpix, cell_width, DGGS_level, NW, NE, SE, SW')

    for row in csvReader: # read through the source file line by line
        if str(row[0]).startswith('ACT'):  # filter to get ACT
        
            #read in the latlong
            longi = float(row[7])
            lati = float(row[6])

            # feed lat long into convertor

            #Pick a (longitude-latitude) point on the ellipsoid and find the cell that contains it ::
            t = (longi, lati)

            #figure resolution to use using longitude
            strLongi = str(longi)  # convert longi to string
            strLati = str(lati)

            longRes = strLongi[::-1].find('.')  #calculate the number of decimals in the longitude
            latiRes = strLati[::-1].find('.')  # calculate the number of decimals in the latitude

            # chose the average Res
            aveRes = (longRes+latiRes)/2

            # adjust this constant to suit the data
            k = 1.7   # have tried 1.7
            resolution = round((aveRes * k) + 1 )

            # keep resloution from being more than 12
            if resolution > 12:
                resolution = 12
            # keep resolution from being less than 7, assume with 4.5 km of where it really is?
            if resolution < 7:
                resolution = 7   # equivalent to within 4.5km of where it really is based on decimal points in lat and long


            # if resolution < 12:
            #     print('Decimal Places ', longRes, 'Calc Resolution ', resolution, 'constant= ', k )
            #     print('aveRes', aveRes, 'from', longRes, latiRes)

            plane = False  # on curve

            w = rdggs.cell_width(resolution)
            if plane:
                area = w**2
            else:
                area =8/(3* math.pi)*w**2

            #calculate the ± error
            # errored = (math.sqrt(area))/2
            #errored = w / 2   # alternative way to calc

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

            # if resolution < 12:
            #     print (dggsLoc)


            c = rdggs.cell(dggsLoc)
            # print (c)
            bound = list()
            # put in try statement for Tasmanian ones that produce an error?
            try:
                for p in c.boundary(n=2, plane=False):
                    bound.append(p)
                    #prepare for shapefile output
                    myPoints.append(str(row[0])+ ', ' + str(row[2]) + ',' + str(thisCell) + ',' + str(p[0]) + ', ' + str(p[1]))

                NW = cleanPosition(str(bound[0]))
                NE = cleanPosition(str(bound[1]))
                SE = cleanPosition(str(bound[2]))
                SW = cleanPosition(str(bound[3]))
                #print(bound)
                #print()

                #build output
                pushout = (str(row[0])+','+ str(row[1])+ ','+ str(row[2])+ ','+ str(row[3])+
                           ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7])+
                           ',' + str(row[8]) + ',' + str(row[9]) + ',' + str(thisCell) + ',' + w +
                          ',' + str(resolution) + ',' + str(NW) + ',' + str(NE) + ',' + str(SE) + ',' + str(SW))

                output.append(pushout)
            except:
                print('failed', str(row[0]), p, c)
                failed += 1   # count the errors
                pass



# output the data to csv files
# overwrites previous file unless you rename or move it
write_list_to_file(output, r"\\xxxxxx\PlaceNames_2018\ACT_PlacesNames2018withDGGS.csv")
#
write_list_to_file(myPoints, r"\\xxxxxx\PlaceNames_2018\ACT_2018PN_boundings.csv")


print ('number failed = ', failed)
#
#for row in output:
#
#    print(row)
#    
print ("finished")

