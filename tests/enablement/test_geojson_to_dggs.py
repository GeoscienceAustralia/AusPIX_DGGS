import pytest
#from auspixdggs.callablemodules.call_DGGS import poly_to_DGGS_tool, line_to_DGGS
from auspixdggs.callablemodules.dggs_in_poly_for_geojson_callable import cells_in_poly
from auspixdggs.callablemodules.dggs_in_line import line_to_DGGS, densify_my_line
import geojson
from geojson.utils import coords
from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon

def get_geojson_by_file(fname):
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
     #print("BBOX {}".format(ret))
     return ret

def get_cells_in_geojson(geojson, resolution):
    list_cells = []
    #print("Type geojson: {}".format(type(geojson)))

    for fea in geojson['features']:  # for feature in attribute table
        #print(fea)
        res_cells = get_cells_in_feature(fea, resolution)
        #print(res_cells)
        #for item in res_cells:
        #    print(item)
        #cell_id_list = [item[0] for item in res_cells]
        cell_id_list = res_cells
        list_cells = list(set(list_cells + list(set(cell_id_list))))
    return list_cells 

def get_cells_in_feature(fea, resolution, cell_obj=True):
    geom = geojson_to_shape(fea['geometry'])
    curr_coords = list(coords(fea))
    thisbbox = bbox(curr_coords)
    cells = []
    if isinstance(geom, LineString) or isinstance(geom, MultiLineString): 
        fea['geometry']['coordinates'] = densify_my_line(fea['geometry']['coordinates'], resolution)
        curr_coords = list(coords(fea))
        print(curr_coords)        
        res_cells = line_to_DGGS(curr_coords, resolution)  # start at DGGS level 10   
        cells = [str(item) for item in res_cells]
    elif isinstance(geom, Polygon) or  isinstance(geom, MultiPolygon):
        res_cells = cells_in_poly(thisbbox, fea['geometry']['coordinates'], resolution)  # start at DGGS level 10    
        print(res_cells)
        cells = [item[0] for item in res_cells]
    else: #try something anyway
        res_cells = cells_in_poly(thisbbox, fea['geometry']['coordinates'], resolution)  # start at DGGS level 10    
        print(res_cells)
        cells = [item[0] for item in res_cells]
    return cells

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
    assert set(test_dggs_lvl10_cells).issubset(set(list_cells)) == True       

if __name__ == "__main__":
    test_complexPolyBasic()
    test_ABS_SA1_black_mountain_geojson_to_DGGS()
    #test_VIC_SA1_Melbourne_CBD_multiple_to_DGGS()
    #test_SA1_flinders_Cape_Barren_multipoly_to_DGGS()
    #test_geojson_line_data()