# -*- coding: utf-8 -*-

''' generate DGGS bounding shapefile from the points
This code suits the "add_DGGS" module
reads a csv of DGGS corners generated by add_DGGS.py
and converts it into a shapefile centroids useing the DGGS cell reference
NB: Not sure of the accuracy of shapefile - seems to be working in total confirmity with other datasets - worked into arcGiS

Joseph Bell Geoscience Australia

'''

import shapefile
import csv
#import dggs
from dggs import RHEALPixDGGS
from dggs import Cell
import ellipsoids
E = ellipsoids.WGS84_ELLIPSOID_DEG
rdggs = RHEALPixDGGS(ellipsoid=E, north_square=1, south_square=2, N_side=3)

from geopy import distance


# read the file
# file with the source data

f = r"\\xxxxx\Geonames_withDGGS.csv"

#set up shapefile for output
w = shapefile.Writer(shapefile.POINT)
w.field('ID', 'C', '20')
w.field('Name', 'C', '70')
w.field('DGGSrHEALPix', 'C', '20')
w.field('LongiWGS84', 'C', '20')  #using 'C' = character = ensures the correct number
w.field('LatiWGS84', 'C', '20')
w.field('Cell_width', 'C', '20')
w.field('Cent_Long', 'C', '20')
w.field('Cent_Lati', 'C', '20')
w.field('fromCent_m', 'C', '20')

counter = 0

with open(f) as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    w.autoBalance = 1
    next(csvReader)  # skip the header
    for row in csvReader: # read through the source file line by line

        # read the DGGS from the file
        thisDGGS = row[12]
        #print(thisDGGS)
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
        nucleus = c.nucleus()
        #print(centroid == nucleus)
        # print('centroid ', centroid)
        # print(thisCell)

        #point for the shape
        w.point(centroid[0], centroid[1])
        # w.record(row[3], row[10])

        thisDGGS = row[12]
        thisWidth = row[13].strip()
        # print(thisDGGS, centroid, 'cell width =', row[11])
        # print(row[2], row[10], float(row[7]), float(row[6]), row[11], 'Centroid =', centroid)


        thisPoint = (float(row[4]), float(row[5]))
        cent = (centroid[1], centroid[0])  # needs to be lat then long for the distance calculation using "distance" imported from geopy
        # print('cent ',cent)
        dist = (distance.vincenty(thisPoint, cent).km) * 1000  # converted to meters

        w.record(ID=row[0], Name=row[2], DGGSrHEALPix=row[12], LongiWGS84=row[5], LatiWGS84=(row[4]),
                 Cell_width=row[13], Cent_Long=centroid[0], Cent_Lati=centroid[1], fromCent_m = dist)


        #myRecord = (row[0] + ', ' + row[1] + ', ' + row[12] + ', ' + row[5] + ', ' + row[4] + ', ' + str(thisWidth) + ', ' + str(centroid[0])+ ', ' + str(centroid[1])+ ', ' + str(dist))
        #
        # if centroid[0] < 0:
        #print(myRecord)

        print("Feature " + str(counter) + " added to Shapefile.")
        counter = counter + 1


w.autoBalance = 1

thisShapeFile = r'shapes/geonames09'
w.save(thisShapeFile)

# project the shapefile into 84
# a simple method of writing a single projection

prj = open("%s.prj" % thisShapeFile, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()

print('finished')


