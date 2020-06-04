# -*- coding: utf-8 -*-

'''
This code calculates all the rHealPix cells in a polygon at the resolution asked for.
It will calculate the DGGS cells and return them to the code.
This example is based on ABS Local Government Areas shapefile.
ESRI not required but it can read the shapefile outputs

Joseph Bell GeoScience Australia

'''


from ..auspixengine.dggs import RHEALPixDGGS

from shapely.geometry import shape, Point, Polygon  # used in the function below ??
# import csv


# make an instance
rdggs = RHEALPixDGGS()

# a function to calculate DGGS cells within a polygon
# mypoly is the shape of the polygon, firstRecord is the first record in attribute table
# resolution is the DGGS resolution required

def poly_to_DGGS_tool(myPoly, thisRecord, resolution):  # one poly and the attribute record for it
    print()
    print()
    # get some info out of the first record
    print('call record', thisRecord)

    # find the bounding bow of the polygon
    bbox = myPoly.bbox
    # print(bbox)
    # [141.3928220030001, -32.01914569999997, 141.5659850120001, -31.883788544999966]

    # now make DGGS points inside the poly based on our desired resolution

    # # an empty list to hold the data
    # cells_in_bbox = list()

    #print bounding box coords
    print('this bbox coords = ', bbox)
    # bboxCent = [((bbox[0] + bbox[2])/2) , (((bbox[1] + bbox[3])/2))]
    # print('bboxCent', bboxCent)
    print()

    # this bbox has the coords around the other way so need to massage them into the correct format
    # bbox = [SW 141.3928220030001, SW -32.01914569999997, NE 141.5659850120001, NE -31.883788544999966]
    # rHealpix requires nw and se coords
    # nw = (0, 45)
    # se = (90, 0)
    # so fixed up it is:
    nw = (bbox[0], bbox[3])
    se = (bbox[2], bbox[1])

    # call function to calculate the cells within the bounding box
    cells = rdggs.cells_from_region(resolution, nw, se, plane=False)
    cell_List = list()
    for row in cells:
        for item in row:
            cell_List.append(item)
            # print(str(item))

    print()
    print('cells found in bbox = ', len(cell_List))
    # for row in cells:
    #     print([str(cell) for cell in row])

    # now find the centroids
    # declare a container to hold bbox centriods list for all the cells
    bboxCentroids = list()
    for cell in cell_List:  # for each cell in the bounding box
        # print(cell, cell.nucleus(plane=False))
        location = cell.nucleus(plane=False)  # on the ellipsoid
        # make a list of cell location and x and y
        thisCentroid = [str(cell), location[0], location[1]]  # adds the xy too
        bboxCentroids.append(thisCentroid)

    # we now have a list of cells within bounding box
    # now filter out the cell centroids that are not inside the actual polygon

    # print(firstShape.points)
    # #######  we are using Shapely to find cells inside the poly. Shapely is good for this.
    # shapely was having trouble with polygons with holes, and in other scripts it has been replaced by hand written code
    # I don't think shapely can import or export any shapefiles, but you can make a list of points that
    # define the shape and give it to shapely
    thisShp = myPoly.points  # this gives a list of points the function input poly has in it
    # now convert to a shapely Polygon
    thisPoly = Polygon(thisShp)  # thisPoly is the Shapely version of the poly

    insidePoly = list()  # declare a new empty list
    # go through the list of DGGS centroids and discover which are 'within' the poly
    for item in bboxCentroids:
        closeCent = bboxCentroids[0]  # save the first centroid in case there are none actually in the polygon
        # print()
        # print('doing ', item)
        point = Point(item[1], item[2])  # make a point from coords
        if point.within(thisPoly):
            insidePoly.append(item[0])
    if len(insidePoly) == 0:
        insidePoly.append(closeCent)
        print('Close cell used')
    print('cells inside poly ', len(insidePoly))  # print the number found
    print('at DGGS resolution = ', resolution)  # print the resolution used

    # return the cells inside the polygon at this DGGS resolution
    return insidePoly



if __name__ == '__main__':
    # main
    pass

print('')

