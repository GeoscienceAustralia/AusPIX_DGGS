# -*- coding: utf-8 -*-

'''
This code calculates all the rHealPix cells in a polygon at the resolution asked for.
It will calculate the DGGS cells and return them to the code.
This example is based on ABS Local Government Areas shapefile.
ESRI not required but it can read the shapefile outputs

Joseph Bell Geoscience Australia

'''


from auspixdggs.auspixengine.dggs import RHEALPixDGGS
from auspixdggs.auspixengine.dggs import Cell
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
myFile = r'\\xxxxxxxxxx\LGA_2018_no_multipart.shp'   #LGS's can be downloaded from ABS?

# read in the file
r = shapefile.Reader(myFile)


# get the attribute table records (combined with shapes) ie shapeRecords
shapeRecs = r.shapeRecords()


# function to write a list to a csv file
# requires the list and the filename to save it too
def write_list_to_file(myList, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in myList:
            outfile.write(entries)
            # add a return after each line
            outfile.write("\n")


# set the resolution between about 2 to 12 - bigger numbers mean smaller cells
# resolution = 9
csvOutput = list()  # initialise
for feature in shapeRecs[0:50]: # slice of x polygons from the whole shapefile
    thisRecord = feature.record[0:] # the attribute table record
    print('len of record', len(thisRecord))
    print(thisRecord)
    print('found LGA called ', thisRecord[2])

    polyShape = feature.shape  # get the spatial component
    polyRecord = feature.record  # get the attributes record (row)
    area = float(feature.record[9])  # needs to point to the area of the polygon in the data sqkm
    print('Area', area)
    #print(type(area))


    resolution = 7   # default resolution
    # vary resolution based on area so bigger areas have bigger cells

    if area < 10:
        resolution = 12
    elif area > 10 and area < 1000.0:
        resolution = 8
    elif area > 1000.0 and area < 30000.0:
        resolution = 6
    elif area > 30000:
        resolution = 4



    print('using resolution ', resolution)
    # calculate the approx cell width at this resolution
    thisWidthApprox = rdggs.cell_width(resolution,
                                       plane=True)  # note only approx because we are using the planar to estimate elipsoidal
    print('++++++++++ Cell width approx  +++', thisWidthApprox, 'm')
    thisLGA = feature.record[1]
    thisName = feature.record[2]

    # call the "call_DGGS" function to return all the DGGS cells (within polygon only)
    cells_in_poly = call_DGGS.poly_to_DGGS_tool(polyShape, polyRecord, resolution)
    print('number in polygon = ', len(cells_in_poly))

    print ('Reducing . . . ')
    # reduce to biggest cells
    theseReducedCells = call_DGGS.coalesce(cells_in_poly)
    #print('reduced cells =', theseReducedCells)
    print('number reduced cells =', len(theseReducedCells))
    # reduce again
    theseReducedCells = call_DGGS.coalesce(theseReducedCells)
    #print('2nd reduced cells =', theseReducedCells)
    print('2nd number reduced cells =', len(theseReducedCells))

    # reduce again
    theseReducedCells = call_DGGS.coalesce(theseReducedCells)
    # print('3nd reduced cells =', theseReducedCells)
    print('3nd number reduced cells =', len(theseReducedCells))

    # reduce again
    theseReducedCells = call_DGGS.coalesce(theseReducedCells)
    # print('3nd reduced cells =', theseReducedCells)
    print('4nd number reduced cells =', len(theseReducedCells))

    # # reduce again
    # theseReducedCells = call_DGGS.coalesce(theseReducedCells)
    # # print('3nd reduced cells =', theseReducedCells)
    # print('5nd number reduced cells =', len(theseReducedCells))



    print(theseReducedCells)

    print()
    print()

    # add this dggs data for eventual output to csv
    # print('myFID = ', str(thisRecord[10]))
    # csvOutput.append(str(thisRecord[10]))
    # csvOutput.append(str(thisRecord[1]))
    # csvOutput.append(thisRecord[2])
    # csvOutput.append(str(theseReducedCells))


    '''
    make a csv to join to the original shapefile
    the csv will key to the shapefile
    this csv will carry the DGGS cells in each polygon'''


    '''
    make a shapefile of the DGGS centroids
    '''

    for thisDGGS in theseReducedCells:

        #print('DGGS = ', thisDGGS)
        #print(theseReducedCells[0:2])
        #build the point
        # find the x y for this DGGS cell
        dggsLoc = list()  # empty list ready to fill
        for char in thisDGGS:  # build a dggs location cell as a list like dggsLoc = ['R', 7, 2, 4, 5, 6, 3, 2, 3, 4, 3, 8, 3]
            if char.isalpha():  # the letter 'R' at the beginning
                dggsLoc.append(char)
            else:
                char = int(char)  # the numbers in the cell
                dggsLoc.append(char)

        c = Cell(rdggs, dggsLoc)
        #print('this is c', c)
        location = c.nucleus(plane=False)  # on the ellipsoid
        # insert the spatial x y into the shape file
        w.point(location[0], location[1])
        # print('location xxxx',location[0], location[1])
        #add the DGGS reference address = cell

        w.record(DGGSrHEALPix=thisDGGS, LongiWGS84=location[0], LatiWGS84=(location[1]), Approx_width= str(thisWidthApprox),
                 DGGS_reso = resolution, LGAcode = thisLGA, Name= thisName, dggs_cell = thisDGGS)

w.autoBalance = 1
print('saving to file . . . ')
thisShapeFile = r'test/LGAtest_02'
w.save(thisShapeFile)

# project the shapefile into 84
# a simple method of writing a single projection

prj = open("%s.prj" % thisShapeFile, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()

# write the csv file  #data needs more formating
# overwrites previous file unless you rename or move it
# write_list_to_file(csvOutput, r'test/LGA_02csvDGGS')


print('finished')


