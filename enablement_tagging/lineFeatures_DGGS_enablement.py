'''
this script converts a shapefile line feature set into DGGS equivalent
- it reads the shapefile then works through line by line figuring out the DGGS cells along that line
- the script calls the points that make up the line, then calculates the DGGS cells for those points
- if the line has sparse points along it, the user may need to 'densify' first
- any duplicated DGGS cells are filtered out
- output is as shapefile for visualiation and integration - note python 2 and python 3 versions of shapefile differ
- could be adapted to also output csv table

'''

import shapefile  #to read and write shapefiles
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance

# identify a shape file to get your lines from
myFile = r'C:\xxxxxxx\test_data\testPoly\waterways_test.shp'

r = shapefile.Reader(myFile) # read in the shapefile file
# get the attribute table records (combined with shapes) ie shapeRecords
shapeRecs = r.shapeRecords()
resolution = 10 # set resolution to be used
doneDGGScells = [] #to accumlate a list of completed cells

#set up shapefile for output
w = shapefile.Writer(shapefile.POLYGON)  # in this case polygons == corners of cells - this is the older verion method
w.field('DGGSrHEALPix', 'C', '20')
w.field('DGGS_reso', 'C', '20')
w.field('thisName', 'C', '20')
w.field('thisHierarchy', 'C', '20')

# now line by line through the attribute table of the source shapefile
for row in shapeRecs:
    polyShape = row.shape  # get the spatial component
    linePoints = polyShape.points
    lineRecord = row.record  # get the attributes record (row)
    for pt in linePoints:  # for each point calculate the DGGS by calling on the DGGS engine
        # ask the engine what cell thisPoint is in
        thisDGGS = rdggs.cell_from_point(resolution, pt, plane=False)# plane=false therefore on the ellipsoid curve
        #add cell if not already in there
        if thisDGGS not in doneDGGScells: # == new one
            doneDGGScells.append(thisDGGS) # save as a done cell
            verts = thisDGGS.vertices(plane = False)  # find the cell corners = vertices from the engine
            w.poly([verts]) #save the polygon spatial data
            # record the attibute table data for this row
            w.record(DGGSrHEALPix=thisDGGS, DGGS_reso=resolution, thisName=lineRecord[3], thisHierarchy=lineRecord[4])

w.autoBalance = 1  # validity check
print('saving to file . . . ')
thisShapeFile = r'C:\Users\u82871\PycharmProjects\AusPIX_DGGS\test_data\testPoly\testLines'
w.save(thisShapeFile)
# now a simple method of writing a single projection so it can be opened in spatial software
prj = open("%s.prj" % thisShapeFile, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
