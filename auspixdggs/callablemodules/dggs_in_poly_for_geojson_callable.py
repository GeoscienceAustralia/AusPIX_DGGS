#import geojson
import pygeoj
from numba import jit,njit
import numpy
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance


def cells_in_poly(bbox, myPoly, resolution, return_cell_obj=False):
    # returns the cells in the poly and lat long of centroid
    ''' 
    a function to calculate DGGS cells within a bounding box then check which ones are in the Polygon
    resolution is the DGGS resolution required  - normally 10 
    myPoly expects a sequence of coordinates
    '''

    # convert the geojson bbox to an AusPIX bounding box
    nw = (bbox[0], bbox[3])
    se = (bbox[2], bbox[1])
    #print('nw', nw, 'se', se)

    # for S region - alternate method work around - needs a list grid of points in the area of interest - then ask for the cell each is in
    # bbox_myPoints = point_set_from_bounds(resolution, nw, se)
    # cell_list = []
    # for pt in bbox_myPoints:
    #     thiscell = rdggs.cell_from_point(resolution, pt, plane=False)
    #     if thiscell not in cell_list:
    #         cell_list.append(thiscell)

    # call function to calculate all the cells within the bounding box  - this function is not working properly in the S area (southern Tas and Antartica
    # - use point_set_from_bounds function (above) instead
    cells = rdggs.cells_from_region(resolution, nw, se, plane=False)  # upper left and down right

    cell_List = list()
    for row in cells:  # gives it to you as a list of lists, so double loop to get them out
        for item in row:
            cell_List.append(item)
    print()
    print('num cells in bb = ', len(cell_List))

    # now find the centroids of those cells using dggs engine
    bboxCentroids = []  # declare a container to hold bbox centriods list for all the cells
    for cell in cell_List:  # for each cell in the bounding box
        location = cell.nucleus(plane=False)  # centroid on the ellipsoid
        if return_cell_obj:
            thisCentroid = [cell, location[0], location[1]]  # adds the xy too 
        else :
            thisCentroid = [str(cell), location[0], location[1]]  # adds the xy too
        bboxCentroids.append(thisCentroid)

    # we now have a list of centroids within bounding box
    # now filter out the cell centroids that are not inside the actual polygon
    insidePoly = list()

    numPoints = len(myPoly)
    print('total vertex in this poly', numPoints)

    edgeData = list()  # we are going to make a list of edges based on pairs of points
    #sort out the parts
    
    for thisFeature in myPoly:
        # print()
        # print('outer', item)
        n = 0
        for thing in thisFeature:
            if n == 0:
                #print('new poly', thing)
                n += 1
            else:
                print('hole in poly', thing)


            previous = (0, 0)  # placeholder for previous point
            for vertex in thing:
                print(vertex)
                if previous != (0, 0):  # not the beginning
                    newEdge = (previous, vertex)
                    #print('new edge', newEdge)
                    edgeData.append(newEdge)
                    #print(edgeData)
                    previous = vertex  # remember for the next interation
                else:
                    previous = vertex

    # now we have a list of edges with a point on each end - all up it describes the poly
    print('number of edges', len(edgeData))

    # now check if this centroid point is in poly
    npthings = []
    npholes = []
    for thisFeature in myPoly:
        n = 0
        for thing in thisFeature:
            npthing=numpy.array(thing)
            if n == 0:
                #print('new poly', thing)
                n += 1
                npthings.append(npthing)
            else:
                print('hole in poly', thing)
                npholes.append(npthing)

    for myPoint in bboxCentroids:
        # this code derived from scratch and has been applied to big jobs successfully
        east = 0
        x = myPoint[1]
        y = myPoint[2]
        # print('prev', previous)
        inPoly = False
        really = True
        for npthing in npthings:
            inPoly = ray_tracing(x,y, npthing)
            if inPoly:
                break
        
        for npthing in npholes:
            really = not ray_tracing(x,y, npthing)
            if not really:
                break  

        if inPoly and really:
            insidePoly.append(myPoint) # add to the cells in the poly

    return insidePoly

def get_dggs_cell_bbox(dggs_cell):
    verts = dggs_cell.vertices(plane=False)  # find the cell corners = vertices from the engine
    verts.append(verts[0]) #add the first point to the end to make a closed poly
    return verts

def get_dggs_cell_geojson_geom(dggs_cell):
    bbox = get_dggs_cell_bbox(dggs_cell)
    geometry = {"type": "Point", "coordinates": bbox}
    return geometry
    
def point_set_from_bounds(resolution, ul, dr):
    # designed to replace rdggs.cells_from_region - which didn't work in the S (Antartic) zone
    # a function to fill a bounding box with xy values (pointset) as seed points to build the set of cells from
    # works across the R to S divide even in the same polygon
    step = 0.0001  # adjust step to suit DGGS resolution  in degrees Lat long - need improvement to help speed it up too
    if resolution == 10:
        step = 0.0015  # OK setting for resolution 10
    pointset = []
    for i in numpy.arange(ul[0], dr[0], step):
        for n in numpy.arange(dr[1], ul[1], step):
            #print('i and n = ', i, n)
            newpt = [i, n]
            pointset.append(newpt)
    return pointset

# line intersection function
@jit(nopython=True)
def ray_tracing(x,y,poly):
    # from https://stackoverflow.com/a/48760556  
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside



if __name__ == '__main__':
    #testfile = pygeoj.load(filepath=r'D:\CSIRO\Test\BlackMountain3.geojson')
    testfile = pygeoj.load(filepath=r'./test_data/ComplexPolyBasic.geojson')


    print('len', len(testfile)) # the number of features
    print('bbox', testfile.bbox) # the bounding box region of the entire file

    my_bbox = testfile.bbox
    resolution = 10
    # calc cell area
    resArea = (rdggs.cell_area(resolution, plane=False))

    # for item in cells_inbb:
    #     print(item)


    #metadata
    print('crs', testfile.crs) # the coordinate reference system
    print('attributes', testfile.all_attributes) # retrieves the combined set of all feature attributes
    print('common attributes', testfile.common_attributes) # retrieves only those field attributes that are common to all features
    print()

    # make an output file of DGGS centroid points with the at atttibute properties
    newfile = pygeoj.new()  # default projection is WGS84

    #work through the features (polygons) one by one and ask for DGGS cells
    for feature in testfile:
        print('first xxx ', feature.properties)  # the feature attributes - want to keep for output
        print()
        #print('bbox', feature.geometry.bbox)  # the bounding box of the feature
        fea_bbox = feature.geometry.bbox
        print(feature.geometry.coordinates)

        this_poly_cells = cells_in_poly(fea_bbox, feature.geometry.coordinates, resolution)  # returns the cells in the poly and lat long of centroid

        print('num cells in this poly =', len(this_poly_cells))
        print('cellx', this_poly_cells)

        for item in this_poly_cells:
            coords = [item[1], item[2]] # the long and lat
            my_prop = feature.properties
            my_Cell = {"AusPIX_DGGS": item[0], "LongiWGS84": item[1], "LatiWGS84": item[2], "CellArea_M2": resArea}

            #include the AusPIX cell information in attributes
            these_attributes = dict(list(my_Cell.items()) + list(my_prop.items()))
            #print('these attributes = ', these_attributes)

            newfile.add_feature(properties=these_attributes, geometry={"type": "Point", "coordinates": coords})



    newfile.save("ComplexPolyBasicResult.geojson")  # will save where the script is run from unless the parth is specified

