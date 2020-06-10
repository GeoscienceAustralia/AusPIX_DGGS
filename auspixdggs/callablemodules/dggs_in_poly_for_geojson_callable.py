#import geojson
import pygeoj
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
                print('new poly', thing)
                n += 1
            else:
                print('hole in poly', thing)


            previous = (0, 0)  # placeholder for previous point
            for vertex in thing:
                print(vertex)
                if previous != (0, 0):  # not the beginning
                    newEdge = (previous, vertex)
                    # print('new edge', newEdge)
                    edgeData.append(newEdge)
                    previous = vertex  # remember for the next interation
                else:
                    previous = vertex

    # now we have a list of edges with a point on each end - all up it describes the poly
    print('number of edges', len(edgeData))

    # now check if this centroid point is in poly
    for myPoint in bboxCentroids:
        # this code derived from scratch and has been applied to big jobs successfully

        x = myPoint[1]
        y = myPoint[2]
        east = 0
        # print('prev', previous)
        for pair in edgeData:
            # for each edge pair of points, see if that edge crosses the y of the point
            if (pair[0][1] < y and pair[1][1] >= y) or (
                    pair[0][1] > y and pair[1][1] <= y):  # yes crosses the point y value

                # if both x's are east of test dggs point then only count
                if (pair[0][0] > x) and (pair[1][0] > x):  # then count
                    # this point is definitly east
                    east += 1

                # if one x is east and one is west then need to calculate
                if (pair[0][0] < x) and (pair[1][0] > x) or (pair[0][0] > x) and (pair[1][0] < x):
                    # print('straddles on x dimension')
                    # work out intersection useing shapely
                    A = (pair[0][0], pair[0][1])  # edge starting  X and Y
                    B = (pair[1][0], pair[1][1])  # edge finishing X and Y
                    # print(A, B)

                    C = (90.0, y)  # adjust if outside Australia
                    D = (179.0, y)  # adjust if outside Australia

                    slope_A = slope(A, B)
                    slope_B = slope(C, D)
                    y_int_A = y_intercept(A, slope_A)
                    y_int_B = y_intercept(C, slope_B)
                    intersect = (line_intersect(slope_A, y_int_A, slope_B, y_int_B))
                    if float(intersect[0]) > x:  # this one is to the east
                        # print('intersect', intersect)
                        east = east + 1
                # if totally west ingnore it
        mod = east % 2
        if mod > 0:
            inPoly = True
        else:
            inPoly = False
        if inPoly:
            insidePoly.append(myPoint) # add to the cells in the poly
            #print(myPoint[0])

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
def slope(P1, P2):
    # dy/dx
    # (y2 - y1) / (x2 - x1)
    return(P2[1] - P1[1]) / (P2[0] - P1[0])
# line intersection function
def y_intercept(P1, slope):
    # y = mx + b
    # b = y - mx
    # b = P1[1] - slope * P1[0]
    return P1[1] - slope * P1[0]
# line intersection function
def line_intersect(m1, b1, m2, b2):
    if m1 == m2:
        print ("These lines are parallel!!!")
        return None

    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return x,y




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

