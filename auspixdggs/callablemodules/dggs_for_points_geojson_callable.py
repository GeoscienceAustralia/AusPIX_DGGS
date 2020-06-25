import pygeoj
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
from auspixdggs.callablemodules.util import transform_coordinates, latlong_to_DGGS

rdggs = RHEALPixDGGS() # make an instance

'''
developed at Geoscience Australia by Joseph Bell June 2020
'''

def dggs_cells_for_points(geojson, resolution):
    # make an output file of DGGS centroid points with the at atttibute properties
    newfile = pygeoj.new()  # default projection is WGS84
    resArea = (rdggs.cell_area(resolution, plane=False))

    #work through the features (polygons) one by one and ask for DGGS cells
    for feature in testfile:
        print('feature attributes ', feature.properties)  # the feature attributes - want to keep for output

        coords = feature.geometry.coordinates  # xy
        print('geom', coords)
        
        #this_dggs_cell = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve
        this_dggs_cell = latlong_to_DGGS(coords, resolution)

        print('found cell = ', this_dggs_cell)

        my_prop = feature.properties
        my_Cell = {"AusPIX_DGGS": str(this_dggs_cell), "LongiWGS84": coords[0], "LatiWGS84": coords[1], "CellArea_M2": resArea}

        #include the AusPIX cell information in attributes
        these_attributes = dict(list(my_Cell.items()) + list(my_prop.items()))
        #print('these attributes = ', these_attributes)

        newfile.add_feature(properties=these_attributes, geometry={"type": "Point", "coordinates": coords})

    #save the ouput geojson file
    newfile.save("test_points.geojson")  # saves into the folder where you have the script - edit to change

if __name__ == '__main__':
    testfile = pygeoj.load(filepath=r'test_data/EIT_geojson_example.geojson')
    resolution = 10

    print('len', len(testfile)) # the number of features
    print('bbox of entire file', testfile.bbox) # the bounding box region of the entire file
    dggs_cells_for_points(testfile, resolution)
