from auspixdggs.callablemodules.dggs_in_poly_for_geojson_callable import cells_in_poly, get_dggs_cell_bbox
from auspixdggs.callablemodules.dggs_in_line import line_to_DGGS
import geojson
from geojson.utils import coords
from geojson import Feature, FeatureCollection
from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon
import json

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
        list_cells = list(list_cells + res_cells)
    return list_cells 

def get_cells_in_feature(fea, resolution, cell_obj=True):
    #print("Type fea: {}".format(type(fea)))
    geom = geojson_to_shape(fea['geometry'])
    #print("Type geom: {}".format(type(geom)))
    curr_coords = list(coords(fea))
    thisbbox = bbox(curr_coords)
    #cells = poly_to_DGGS_tool(polygon, '', 10, input_bbox=thisbbox)  # start at DGGS level 10   
    #listPolyCoords = list(polygon.exterior.coords)
    cells = []
    if isinstance(geom, LineString) or isinstance(geom, MultiLineString): 
        #res_cells = line_to_DGGS(geom, resolution)  # start at DGGS level 10   
        res_cells = line_to_DGGS(curr_coords, resolution)  # start at DGGS level 10   
        cells = res_cells
    elif isinstance(geom, Polygon) or  isinstance(geom, MultiPolygon):
        res_cells = cells_in_poly(thisbbox, curr_coords, resolution, return_cell_obj=True)  # start at DGGS level 10    
        print(res_cells)
        cells = [item[0] for item in res_cells]
    else: #try something anyway
        cells = cells_in_poly(thisbbox, curr_coords, resolution, return_cell_obj=True)  # start at DGGS level 10    
        print(res_cells)
        cells = [item[0] for item in res_cells]

    return cells

def transform_ABS_SA1_black_mountain_geojson_to_DGGS():
    # read in the file
    geojson_input = get_geojson_by_file('test_data/ACT_SA1_Black_Mountain.geojson')
    test_dggs_lvl10_cells = ['R7852347722', 'R7852348371']
    resolution = 10
    list_cells = get_cells_in_geojson(geojson_input, 10)    
    list_features = []
    for cell in list_cells:
        #print(cell.vertices(plane=False))
        bbox_coords = get_dggs_cell_bbox(cell)
        #print(bbox_coords)
        geom_obj = Polygon(bbox_coords)
        feat = Feature(geometry=geom_obj, properties={"dggs_cell_id": str(cell)}) 
        #print(feat)
        list_features.append(feat)

    feature_collection = FeatureCollection(list_features)
    print(feature_collection)

    geojson_dump = geojson.dumps(feature_collection, indent=4, sort_keys=True)
    print(geojson_dump)
    with open('poly.geojson', 'w') as json_file:
        data = geojson.dump(feature_collection, json_file, indent=4, sort_keys=True)        


def transform_geojson_line_data():
    # read in the file
    geojson_input = get_geojson_by_file('test_data/SA_RoadsExample_lines.geojson')
    list_cells = []
    resolution = 10
    test_dggs_lvl10_cells = ['R7751215231', 'R7751215230', 'R7751223885', 'R7751218502']
    list_cells = get_cells_in_geojson(geojson_input, resolution)
    list_features = []
    for cell in list_cells:
        #print(cell.vertices(plane=False))
        bbox_coords = get_dggs_cell_bbox(cell)
        #print(bbox_coords)
        geom_obj = Polygon(bbox_coords)
        feat = Feature(geometry=geom_obj, properties={"dggs_cell_id": str(cell)}) 
        #print(feat)
        list_features.append(feat)

    feature_collection = FeatureCollection(list_features)
    print(feature_collection)

    geojson_dump = geojson.dumps(feature_collection, indent=4, sort_keys=True)
    print(geojson_dump)
    with open('line.geojson', 'w') as json_file:
        data = geojson.dump(feature_collection, json_file, indent=4, sort_keys=True)    


if __name__ == "__main__":
   transform_ABS_SA1_black_mountain_geojson_to_DGGS()
   transform_geojson_line_data()
