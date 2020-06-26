import pygeoj
from dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance
import math

'''
developed by Joseph Bell at Geoscience Australia June 2020
'''
def densify_my_line(line_to_densify, resolution):
    '''
    densify a line based on the resolution of the cells
    designed to return a continuous string of ajoining DGGS cells along a line feature
    '''

    resArea = (rdggs.cell_area(resolution, plane=False))  # ask engine for area of cell
    # math to define a suitable distance between vertices - ensures good representation of the line - a continuous run of cells to define the line
    min_dist = math.sqrt(float(resArea))/300000  # width of cell changes with sqrt of the area - 300000 is a constant that can be changed but will change output

    try:
        # first try multi-line construct (on failure try single line)
        for line_points in line_to_densify:
            edgeData = []  # we are going to make a list of edges based on pairs of vertices
            previous = (0, 0)  # placeholder for previous point
            for vertex in line_points:
                #print(vertex)
                if previous != (0, 0):  # not the beginning
                    newEdgeMulti = (previous, vertex)
                    #print('new edge', newEdge)
                    edgeData.append(newEdgeMulti)
                    previous = vertex  # remember for the next iteration
                else:
                    previous = vertex
            # now calculate the length of segment
            new_line = []
            for edge in edgeData:
                dx = edge[1][0] - edge[0][0]
                dy = edge[1][1] - edge[0][1]
                #print('dxdy', dx, dy)
                line_length = math.sqrt((dx*dx) + (dy*dy))  # length in degrees
                segments = round(line_length / min_dist)  # figure number of segments needed
                if segments == 0:  # cannot be 0
                    segments = 1  # chage zero to to one
                densified_line = (split([edge[1][0], edge[1][1]], [edge[0][0], edge[0][1]], segments))  #using split function below

                new_line.append(densified_line)  # add this segment into the output line

    except:
        # try for single line construct
        edgeData = []  # we are going to make a list of edges based on pairs of vertices
        previous = (0, 0)  # placeholder for previous point
        for vertex in line_to_densify:  # this is the outer [] for multi-line object
            if previous != (0, 0):  # not the beginning
                newEdge = (previous, vertex)
                print('new edge', newEdge)
                edgeData.append(newEdge)
                previous = vertex  # remember for the next iteration
            else:
                previous = vertex
            # now calculate the length of segment
            new_line = []
        for segment in edgeData:
            print('segment', segment)
        for edge in edgeData:
            print('myEdge', edge)
            dx = edge[1][0] - edge[0][0]
            dy = edge[1][1] - edge[0][1]
            #print('dxdy', dx, dy)
            line_length = math.sqrt((dx*dx) + (dy*dy))  # length in degrees
            segments = round(line_length / min_dist)  # figure number of segments needed
            if segments == 0:  # cannot be 0
                segments = 1  # chage zero to to one
            densified_line = (split([edge[1][0], edge[1][1]], [edge[0][0], edge[0][1]], segments))  #using split function below

            new_line.append(densified_line)  # add this segment into the output line

    if len(new_line) == 0:
    print('error nothing returned')
    return new_line  # we return this line in the datset with extra points along it (densified)

# OLD multiline function deleted


def split(start, end, segments):
    '''
   add vertices to a line to densify
   must decide on how many segments you need using the densify_my_line function above
   usually called from the densify_my_line function
    '''
    x_delta = (end[0] - start[0]) / float(segments)
    y_delta = (end[1] - start[1]) / float(segments)
    points = []
    for i in range(1, segments):
        points.append([start[0] + i * x_delta, start[1] + i * y_delta])
    return [start] + points + [end]


def dggs_enable_line(thisfile, myOutput_location_and_name, resolution):
    '''  takes a geojson file and adds AusPix DGGS cell information at the resolution called for
    maintains any properties data for out but at the end
    AusPix data in the first columns - then the properties data
    '''

    # calc cell area in m2
    resArea = (rdggs.cell_area(resolution, plane=False))

    # metadata
    print('number of features', len(thisfile))  # the number of features
    print('bbox of entire file', thisfile.bbox)  # the bounding box region of the entire file
    print('area of each cell at this resolution', resArea)
    print('crs', thisfile.crs)  # the coordinate reference system
    print('attributes', thisfile.all_attributes)  # retrieves the combined set of all feature attributes
    print('common attributes',
          thisfile.common_attributes)  # retrieves only those field attributes that are common to all features
    print()

    # make an output file of DGGS centroid points with the at atttibute properties
    newfile = pygeoj.new()  # default projection is WGS84

    #work through the features (polygons) one by one and ask for DGGS cells
    for feature in thisfile:   #each feature is an individual line
        print('feature attributes ', feature.properties)  # the feature attributes - want to keep for output

        coords = feature.geometry.coordinates  # xy's along line
        print('in_coords= ', (coords))
        densified_coords = densify_my_line(coords, resolution)
        print('out coords = ', (densified_coords))

        for item in densified_coords:
            doneDGGScells = []
            for coords in item:  # for this road or sreat line look at all the points that describe it
                #print('thispt', coords)
                thisDGGS = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve
                if thisDGGS not in doneDGGScells:  # == new one
                    doneDGGScells.append(thisDGGS)  # save as a done cell
                    verts = thisDGGS.vertices(plane=False)  # find the cell corners = vertices from the engine
                    #print('v', verts[0])
                    verts.append(verts[0]) #add the first point to the end to make a closed poly
                    #print('verts', verts)

                    my_prop = feature.properties
                    my_Cell = {"AusPIX_DGGS": str(thisDGGS), "CellArea_M2": resArea}

                    #include the AusPIX cell information in attributes
                    these_attributes = dict(list(my_Cell.items()) + list(my_prop.items()))
                    #print('these attributes = ', these_attributes)

                    newfile.add_feature(properties=these_attributes, geometry={"type": "Polygon", "coordinates": [verts]})

    #save the ouput geojson file
    newfile.save(myOutput_location_and_name + '.geojson')  # saves into the folder where you have the script - edit to change

if __name__ == "__main__":

    thisfile = pygeoj.load(filepath=r'D:\CSIRO\test_lines_for_densification.geojson')
    resolution = 10

    #call function
    dggs_enable_line(thisfile, 'test_lineOUT_DGGSed', resolution)
