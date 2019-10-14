'''
this script uses the DGGS engine to calculate the DGGS cells within a polygon
- it reads in a shapefile, but could be adapted to read in other spatial info - eg postGIS
- outputs another shapefile for visualisation and integration
- could also be adapted to export as csv or triple etc
- depends on the 'dggs_in_poly' GA module which does much of the work - see AusPIX enablement folder Git

Written by Joseph Bell at Geoscience Australia 2019
'''

import shapefile  #to read and write shapefiles
import dggs_in_poly  # this is script written by GA - see GitHub AusPix DGGS enablement folder
from dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance

# identify a shape file to get your polygons from
myFile = r'C:\xxxxxxxxxx\AusPIX_DGGS\test_data\testPoly\testPoly3.shp'

r = shapefile.Reader(myFile) # read in the file
# get the attribute table records (combined with shapes) ie shapeRecords
shapeRecs = r.shapeRecords()
resolution = 8 # set resolution to be used

#set up shapefile for output
w = shapefile.Writer(shapefile.POINT)  # in this case points == centroids of cells
w.field('DGGSrHEALPix', 'C', '20')
w.field('LongiWGS84', 'C', '20')  #using 'C' = character = ensures the correct number
w.field('LatiWGS84', 'C', '20')
w.field('DGGS_reso', 'C', '20')
w.field('SA1code', 'C', '20')
w.field('SA2Name', 'C', '20')

# now line by line through the attribute table of the source shapefile
for row in shapeRecs:
    polyShape = row.shape  # get the spatial component
    polyRecord = row.record  # get the attributes record (row)
    # call the "poly_to_DGGS_tool" function to return all the DGGS cells (within each polygon) includes long & lat
    cells_in_poly = dggs_in_poly.poly_to_DGGS_tool(polyShape, resolution)
    # cells_in_poly == list of [DGGSid , longitude of centroid, latitude of centroid]
    print('number in polygon = ', len(cells_in_poly))
    thisSA1 = polyRecord[0]  #SA1 code
    thisName = polyRecord[4] #SA2 name
    #go through the cells one by one - build them into the new attribute table
    #make a shapefile of the DGGS centroids
    for dggs_cell in cells_in_poly:
        longitude = dggs_cell[1]
        latitude = dggs_cell[2]
        w.point(longitude, latitude)# insert the spatial x y into the shapefile
        w.record(DGGSrHEALPix=dggs_cell[0], LongiWGS84=longitude, LatiWGS84=(latitude), DGGS_reso = resolution, SA1code = thisSA1, SA2Name= thisName)


w.autoBalance = 1
print('saving to file . . . ')
thisShapeFile = r'C:\xxxxxxx\PycharmProjects\AusPIX_DGGS\test_data\testPoly\testPoly3_with_DGGS2.shp'
w.save(thisShapeFile)
# a simple method of writing a single projection so it can be opened in spatial software
prj = open("%s.prj" % thisShapeFile, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()
