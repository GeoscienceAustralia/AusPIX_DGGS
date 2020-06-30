import pytest
import geojson
from geojson.utils import coords
from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon
from auspixdggs.callablemodules.dggs_in_poly_for_geojson_callable import cells_in_poly
from auspixdggs.callablemodules.dggs_in_line import line_to_DGGS, densify_my_line
from auspixdggs.callablemodules.util import geojson_to_shape, bbox, get_cells_in_feature, get_cells_in_geojson

def get_geojson_by_file(fname):
    data = None
    with open(fname) as json_file:
        data = geojson.load(json_file)
    return data

def test_ABS_SA1_black_mountain_geojson_to_DGGS():
    # read in the file
    geojson = get_geojson_by_file('test_data/ACT_SA1_Black_Mountain.geojson')
    test_dggs_lvl10_cells = ['R7852347722', 'R7852348371']
    resolution = 10
    list_cells = get_cells_in_geojson(geojson, 10)    
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True


def test_complexPolyBasic():
    # read in the file
    geojson = get_geojson_by_file('test_data/ComplexPolyBasic.geojson')
    test_dggs_lvl10_cells = ['R7852620003', 'R7852612225']
    resolution = 10
    list_cells = get_cells_in_geojson(geojson, 10)    
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True

def test_NSW_SA1_sydney_haymarket_geojson_to_DGGS():
    # read in the file
    geojson = get_geojson_by_file('test_data/NSW_SA1_Sydney_Haymarket.geojson')
    test_dggs_lvl10_cells = ['R8607065772', 'R8607068112']
    resolution = 10
    list_cells = get_cells_in_geojson(geojson, 10)    
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True      


def test_VIC_SA1_Melbourne_CBD_multiple_to_DGGS():
    # read in the file
    geojson = get_geojson_by_file('test_data/VIC_SA1_Melbourne_CBD_multiple.geojson')
    test_dggs_lvl10_cells = ['R7847710830', 'R7847710752']
    resolution = 10
    list_cells = get_cells_in_geojson(geojson, 10)    
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True  

#disabling this test as the bbox is quite large and test runs slow
#def test_SA1_flinders_Cape_Barren_multipoly_to_DGGS():
def try_SA1_flinders_Cape_Barren_multipoly_to_DGGS():
    # read in the file
    geojson = get_geojson_by_file('test_data/ABS_SA1_Flinders_Cape_Barren_Islands_multipoly.geojson')
    test_dggs_lvl10_cells = ['R7847710830', 'R7847710752']
    resolution = 10
    list_cells = get_cells_in_geojson(geojson, 10)    
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True       


def test_geojson_line_data():
    # read in the file
    geojson = get_geojson_by_file('test_data/SA_RoadsExample_lines.geojson')
    list_cells = []
    resolution = 3
    test_dggs_lvl10_cells = ['R7751215231', 'R7751215230', 'R7751223885', 'R7751218502']

    list_cells = get_cells_in_geojson(geojson, 10)
    list_cells = [str(cell) for cell in list_cells]
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True       

if __name__ == "__main__":
    test_complexPolyBasic()
    test_ABS_SA1_black_mountain_geojson_to_DGGS()
    #test_VIC_SA1_Melbourne_CBD_multiple_to_DGGS()
    #test_SA1_flinders_Cape_Barren_multipoly_to_DGGS()
    #test_geojson_line_data()