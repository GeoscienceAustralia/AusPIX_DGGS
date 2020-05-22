import pytest
import shapefile
from pyproj import Proj, transform
import json
from auspixdggs.callablemodules.call_DGGS import poly_to_DGGS_tool
import geojson
from geojson.utils import coords

def get_shp(fname):
    return shapefile.Reader(fname)

def get_geojson(fname):
    data = None
    with open(fname) as json_file:
        data = geojson.load(json_file)
    return data

def test_ABS_SA1_shp_to_DGGS():
    """Test integrity of ABS SA1 2016 SHP SA1 Black Mountain feature enablement to DGGS
    """
    validFlag = False
    shape = get_shp('test_data/ACT_SA1_Black_Mountain.geojson')
    feature = shape.shapeRecords()[0]
    first = feature.shape.__geo_interface__  

    print(first)

def bbox(coord_list):
     box = []
     for i in (0,1):
         res = sorted(coord_list, key=lambda x:x[i])
         box.append((res[0][i],res[-1][i]))
     ret = f"({box[0][0]} {box[1][0]}, {box[0][1]} {box[1][1]})"
     return ret

def test_ABS_SA1_geojson_to_DGGS():
    # read in the file
    geojson = get_geojson('test_data/ACT_SA1_Black_Mountain.geojson')

    for fea in geojson['features']:  # for feature in attribute table
        fea['bbox'] = bbox(list(coords(fea)))
        cells = poly_to_DGGS_tool(fea, '', 10)  # start at DGGS level 10
        for item in cells:
             print(item)

if __name__ == "__main__":
    test_ABS_SA1_geojson_to_DGGS()