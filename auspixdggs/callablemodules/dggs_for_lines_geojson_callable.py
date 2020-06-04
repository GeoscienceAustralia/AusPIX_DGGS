import pygeoj
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance

'''
developed by Joseph Bell at Geoscience Australia June 2020
'''


def dggs_enable_line(thisfile, myOutput_location_and_name, resolution):
    '''  takes a geojson file and adds AusPix DGGS cell information at the resolution called for
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
    for feature in thisfile:
        print('feature attributes ', feature.properties)  # the feature attributes - want to keep for output

        coords = feature.geometry.coordinates  # xy
        #print('geom', coords)

        for item in coords:
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

    thisfile = pygeoj.load(filepath=r'D:\CSIRO\Test\lines_desified_no_tracks.geojson')
    resolution = 11

    #call function
    dggs_enable_line(thisfile, 'D:\CSIRO\Test\lines_desified_no_tracks_DGGSed', resolution)
