import pytest
import shapefile
from pyproj import Proj, transform
import json
from auspixdggs.callablemodules.call_DGGS import poly_to_DGGS_tool
import geojson
from geojson.utils import coords
from shapely.geometry import Polygon, shape
from os import listdir
from os.path import isfile, join
from json import JSONDecodeError


def get_geojson_by_file(fname):
    data = None
    with open(fname) as json_file:
        data = geojson.load(json_file)
    return data

def geojson_to_shape(g):
    return shape(g) 

def display_geojson_types(g):
    for fea in g['features']:  # for feature in attribute table
        print("Type fea: {}".format(type(fea)))
        polygon = geojson_to_shape(fea['geometry'])
        print("Type polygon: {}".format(type(polygon)))

def test_check_testdata_geojson_valid():
    # read in the file    
    directory = "test_data"
    files = [join(directory, f) for f in listdir(directory) if (isfile(join(directory, f)) and f.endswith(".geojson"))]
    print(files)
    #files = [
    #    'test_data/ACT_SA1_Black_Mountain.geojson',
    #    'test_data/NSW_SA1_Sydney_Haymarket.geojson',
    #    'test_data/VIC_SA1_Melbourne_CBD_multiple.geojson',
    #    'test_data/ABS_SA1_Flinders_Cape_Barren_Islands_multipoly.geojson',
    #    'test_data/SA_RoadsExample_lines.geojson'
    #]
    for f in files:
        isListOfFilesValid = True
        print(f)
        try:
            g = get_geojson_by_file(f)
            display_geojson_types(g)
        except JSONDecodeError: 
            isListOfFilesValid = False
            break
        except ValueError as e:
            isListOfFilesValid = False
            print("Error found in {}: {}".format(f,e))
        assert isListOfFilesValid == True
        print()

        

if __name__ == "__main__":
    test_check_testdata_geojson_valid()
  