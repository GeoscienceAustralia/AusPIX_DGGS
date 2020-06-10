import pygeoj
from dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance

'''
developed at Geoscience Australia by Joseph Bell June 2020
'''
testfile = pygeoj.load(filepath=r'D:\Grahaeme\EIT_geojson_example.geojson')

print('len', len(testfile)) # the number of features
print('bbox of entire file', testfile.bbox) # the bounding box region of the entire file

resolution = 10
# calc cell area
resArea = (rdggs.cell_area(resolution, plane=False))

#metadata
print('crs', testfile.crs) # the coordinate reference system
print('attributes', testfile.all_attributes) # retrieves the combined set of all feature attributes
print('common attributes', testfile.common_attributes) # retrieves only those field attributes that are common to all features
print()

# make an output file of DGGS centroid points with the at atttibute properties
newfile = pygeoj.new()  # default projection is WGS84

#work through the features (polygons) one by one and ask for DGGS cells
for feature in testfile:
    print('feature attributes ', feature.properties)  # the feature attributes - want to keep for output

    coords = feature.geometry.coordinates  # xy
    print('geom', coords)

    this_dggs_cell = rdggs.cell_from_point(resolution, coords, plane=False)  # false = on the elipsoidal curve

    print('found cell = ', this_dggs_cell)

    my_prop = feature.properties
    my_Cell = {"AusPIX_DGGS": str(this_dggs_cell), "LongiWGS84": coords[0], "LatiWGS84": coords[1], "CellArea_M2": resArea}

    #include the AusPIX cell information in attributes
    these_attributes = dict(list(my_Cell.items()) + list(my_prop.items()))
    #print('these attributes = ', these_attributes)

    newfile.add_feature(properties=these_attributes, geometry={"type": "Point", "coordinates": coords})

#save the ouput geojson file
newfile.save("test_points.geojson")  # saves into the folder where you have the script - edit to change

