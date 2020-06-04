'''
This code calculates all the AusPIX cells in a polygon at the resolutions defined by user.
It will calculate the DGGS cells and return them to the code.

ESRI not required but it can read the shapefile outputs
Joseph Bell Geoscience Australia 2019

'''

from auspixdggs.auspixengine.dggs import RHEALPixDGGS
import shapefile
import numpy


# make an instance
rdggs = RHEALPixDGGS()

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
    # y = mx + b
    # Set both lines equal to find the intersection point in the x direction
    # m1 * x + b1 = m2 * x + b2
    # m1 * x - m2 * x = b2 - b1
    # x * (m1 - m2) = b2 - b1
    # x = (b2 - b1) / (m1 - m2)
    x = (b2 - b1) / (m1 - m2)
    # Now solve for y -- use either line, because they are equal here
    # y = mx + b
    y = m1 * x + b1
    return x,y

def point_set_from_bounds(resolution, ul, dr):
    # designed to replace rdggs.cells_from_region - which didn't work in the S (Antartic) zone 
    # a function to fill a bounding box with xy values (pointset) as seed points to build the set of cells from
    # works across the R to S divide even in the same polygon
    step = 0.0001 # adjust step to suit DGGS resolution  in degrees Lat long - need improvement to help speed it up too
    if resolution == 10:
        step = 0.0015  # OK setting for resolution 10
    pointset = []
    for i in numpy.arange(ul[0], dr[0], step):
        for n in numpy.arange(dr[1], ul[1], step):
            #print('i and n = ', i, n)
            newpt = [i, n]
            pointset.append(newpt)
    return pointset

def poly_to_DGGS_tool(myPoly, resolution):  # one poly and the attribute record for it
    ''' a function to calculate DGGS cells within a polygon
    mypoly is the shape of the polygon
    resolution is the DGGS resolution required '''

    # find the bounding box of the polygon
    bbox = myPoly.bbox
    # now find DGGS points inside the poly based on our desired resolution

    #print('this bbox coords = ', bbox) #print bounding box coords
    # this bbox has the coords around the other way so need to massage them into the correct format
    # bbox = [SW 141.3928220030001, SW -32.01914569999997, NE 141.5659850120001, NE -31.883788544999966]
    # rHealpix requires nw and se coords
    # nw = (0, 45),  # se = (90, 0)
    # so fixed up it is:
    nw = (bbox[0], bbox[3])
    se = (bbox[2], bbox[1])
    #print('nw', nw, 'se', se)

    bbox_myPoints = point_set_from_bounds(resolution, nw, se)
    cell_list = {} 
    for pt in bbox_myPoints:
        thiscell = rdggs.cell_from_point(resolution, pt, plane=False)
        cell_string = str(thiscell)
        cell_list[cell_string] = thiscell


    # # call function to calculate all the cells within the bounding box  - this function is not working properly in the S area
    # used point_set_from_bounds function above instead
    # cells = rdggs.cells_from_region(resolution, nw, se, plane=False)  # upper left and down right

    #cell_List = list()
    # for row in cells:  # gives it to you as a list of lists, so double loop to get them out
    #     for item in row:
    #         cell_List.append(item)
    #         #print(str(item))
    #print('num cells in bb = ', len(cell_list))

    # now find the centroids of those cells using dggs engine
    bboxCentroids = list() # declare a container to hold bbox centriods list for all the cells
    for cell in cell_list.values():  # for each cell in the bounding box
        # print(cell, cell.nucleus(plane=False))
        location = cell.nucleus(plane=False)  # on the ellipsoid
        # make a list of cell location and x and y
        thisCentroid = [str(cell), location[0], location[1]]  # adds the xy too
        #print('thisCent = ', thisCentroid)
        bboxCentroids.append(thisCentroid)

    # we now have a list of centroids within bounding box
    # now filter out the cell centroids that are not inside the actual polygon
    insidePoly = list()

    # first find the end of the file - because the parts only position the start of each part
    numPoints = len(myPoly.points)  # total number of points
    #print('total vertex in poly', numPoints)

    # find the parts of a poly - especially for polys with holes
    parts = myPoly.parts

    #print('parts starting at', parts)
    parts.append(numPoints)  # add the location of the last point to the list for from-to sequencing
    #print('parts', parts)

    edgeData = list()  # we are going to make a list of edges based on pairs of points in each part

    # now build edges
    # for point in range from 0 to number of parts
    # the parts are the outer polygon and any holes in the middle
    for part in range(0, len(myPoly.parts)-1):
    #for i in parts[-2]:
        #print('partsxx', parts)
        thisPolyPoints = list()  # declare an empty list
        # thisPolyPoints = myPoly.points[parts[p]:parts[p + 1]]
        thisRange = [parts[part], 'to' , parts[part+1]]
        # print('this Range', thisRange )

        thisPolyPoints = myPoly.points[parts[part]:parts[part + 1]]   # bracket the range

        # calculate the edges of this poly into edgeDataList
        previous = (0, 0)  # placeholder for prevoius point
        polyStart = (0, 0)  # initial value

        for pt in thisPolyPoints:
            if previous != (0, 0):  # not the begining
                newEdge = (previous, pt)
                # print('new edge', newEdge)
                edgeData.append(newEdge)
                previous = pt  # remember for the next interation

                if pt == polyStart:  # poly has completed
                    previous = (0, 0)  # reset for the next poly part (hole)
            else:
                # remember start of poly
                polyStart = pt
                previous = pt


    # now we have a list of edges

    # check section

    # now check if this centroid point is in poly
    for myPoint in bboxCentroids:
        # this code derived from scratch and seems to be working

        x = myPoint[1]
        y = myPoint[2]
        #print('testing new point', x, y)
        east = 0
        # print('prev', previous)
        for pair in edgeData:
            # for each edge pair of points, see if that edge crosses the y of the point
            if (pair[0][1] < y and pair[1][1] >= y) or (pair[0][1] > y and pair[1][1] <= y): # yes crosses the point y value

                # if both x's are east of test dggs point then only count
                if (pair[0][0] > x) and (pair[1][0] > x):  # then count
                    # this point is definitly east
                    east += 1

                # if one x is east and one is west then need to calculate
                if (pair[0][0] < x) and (pair[1][0] > x) or (pair[0][0] > x) and (pair[1][0] < x):
                    #print('straddles on x dimension')
                    # work out intersection useing shapely
                    A = (pair[0][0], pair[0][1])  # edge starting  X and Y
                    B = (pair[1][0], pair[1][1])  # edge finishing X and Y
                    #print(A, B)

                    C = (90.0, y)  # adjust if outside Australia
                    D = (179.0, y)  # adjust if outside Australia

                    slope_A = slope(A, B)
                    slope_B = slope(C, D)
                    y_int_A = y_intercept(A, slope_A)
                    y_int_B = y_intercept(C, slope_B)
                    intersect = (line_intersect(slope_A, y_int_A, slope_B, y_int_B))
                    if float(intersect[0]) > x: # this one is to the east
                        # print('intersect', intersect)
                        east = east + 1
                        #stradleX += 1
                        # print('new east = ', east)

                # if totally west ingnore it

                #print('east', east)
                #print()

        #print('east', east)
        mod = east % 2
        if mod > 0:   inPoly = True
        else:         inPoly = False


        # print('NEW POINT')

        if inPoly:
            insidePoly.append(myPoint)

    #print('cells in bbox = ', len(bboxCentroids))
    #print('cells inside poly ', len(insidePoly))  # print the number found
    #print('at DGGS resolution = ', resolution)  # print the resolution used
    # print('inside Poly Call_DGGS', insidePoly)
    # return the cells inside the polygon at this DGGS resolution
    #print('strdX', stradleX)

    return insidePoly

if __name__ == '__main__':

    # note this 'main' will not run if called from another module

    testPoly = r"\\xxxxxxxxxxxxx\WaterBodiesNeo\Irrigated_Areas\SampleTest_Irrigation.shp"

    # read in the file
    sf = shapefile.Reader(testPoly)

    # get the attribute table records (combined with shapes)
    irrPolys = sf.shapeRecords()
    # firstShape = shapeRecs[0].shape

    index = 0
    for fea in irrPolys:  # for feature in attribute table
            cells = poly_to_DGGS_tool(fea.shape, 10)  # start at DGGS level 10

    # for item in cellsInPoly:
    #     print(item)
