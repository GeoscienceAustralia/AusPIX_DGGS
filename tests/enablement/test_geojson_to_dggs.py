import pytest
import shapefile
from pyproj import Proj, transform
import json
from auspixdggs.callablemodules.call_DGGS import poly_to_DGGS_tool
import geojson
from geojson.utils import coords
from shapely.geometry import Polygon, shape



def get_geojson(fname):
    data = None
    with open(fname) as json_file:
        data = geojson.load(json_file)
    return data

def geojson_to_shape(g):
    return shape(g)
    


def bbox(coord_list):
     box = []
     for i in (0,1):
         res = sorted(coord_list, key=lambda x:x[i])
         box.append((res[0][i],res[-1][i]))
     #ret = f"({box[0][0]} {box[1][0]}, {box[0][1]} {box[1][1]})"
     ret = [ box[0][0], box[1][0], box[0][1], box[1][1] ]
     print("BBOX {}".format(ret))
     return ret

def test_ABS_SA1_black_mountain_geojson_to_DGGS():
    # read in the file
    geojson = get_geojson('test_data/ACT_SA1_Black_Mountain.geojson')

    for fea in geojson['features']:  # for feature in attribute table
        
        polygon = geojson_to_shape(fea['geometry'])
        thisbbox = bbox(list(coords(fea)))
        cells = poly_to_DGGS_tool(polygon, '', 10, input_bbox=thisbbox)  # start at DGGS level 10
        test_dggs_lvl10_cells = ['R7852347722', 'R7852348371']

        for item in cells:
             print(item)

        assert set(test_dggs_lvl10_cells).issubset(set(cells)) == True


def test_NSW_SA1_sydney_haymarket_geojson_to_DGGS():
    # read in the file
    geojson = get_geojson('test_data/NSW_SA1_Sydney_Haymarket.geojson')

    for fea in geojson['features']:  # for feature in attribute table        
        polygon = geojson_to_shape(fea['geometry'])
        thisbbox = bbox(list(coords(fea)))
        cells = poly_to_DGGS_tool(polygon, '', 10, input_bbox=thisbbox)  # start at DGGS level 10
        test_dggs_lvl10_cells = ['R8607065772', 'R8607068112']
        for item in cells:
             print(item)
        assert set(test_dggs_lvl10_cells).issubset(set(cells)) == True       


def test_VIC_SA1_Melbourne_CBD_multiple_to_DGGS():
    # read in the file
    geojson = get_geojson('test_data/VIC_SA1_Melbourne_CBD_multiple.geojson')
    list_cells = []

    for fea in geojson['features']:  # for feature in attribute table        
        polygon = geojson_to_shape(fea['geometry'])
        thisbbox = bbox(list(coords(fea)))
        cells = poly_to_DGGS_tool(polygon, '', 10, input_bbox=thisbbox)  # start at DGGS level 10

        for item in cells:
             print(item)
             if(isinstance(item, list)):
                list_cells.append(item[0])                 
                
             else:
                list_cells.append(item)
        #list_cells = list_cells + cells

    test_dggs_lvl10_cells = ['R7847710830', 'R7847710752']
    print(list_cells)
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True       

#disabling this test as the bbox is quite large and test runs slow
#def test_SA1_flinders_Cape_Barren_multipoly_to_DGGS():
def try_SA1_flinders_Cape_Barren_multipoly_to_DGGS():
    # read in the file
    geojson = get_geojson('test_data/ABS_SA1_Flinders_Cape_Barren_Islands_multipoly.geojson')
    list_cells = []

    for fea in geojson['features']:  # for feature in attribute table        
        polygon = geojson_to_shape(fea['geometry'])
        thisbbox = bbox(list(coords(fea)))
        cells = poly_to_DGGS_tool(polygon, '', 10, input_bbox=thisbbox)  # start at DGGS level 10

        for item in cells:
             print(item)
             if(isinstance(item, list)):
                list_cells.append(item[0])                 
                
             else:
                list_cells.append(item)
        #list_cells = list_cells + cells

    test_dggs_lvl10_cells = ['R7847710830', 'R7847710752']
    print(list_cells)
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True       


if __name__ == "__main__":
    #test_ABS_SA1_shp_to_DGGS()
    #test_ABS_SA1_black_mountain_geojson_to_DGGS()
    #test_VIC_SA1_Melbourne_CBD_multiple_to_DGGS()
    #test_SA1_flinders_Cape_Barren_multipoly_to_DGGS()