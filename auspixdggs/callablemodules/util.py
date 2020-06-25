from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon,  Point, MultiPoint
from geojson.utils import coords
from auspixdggs.callablemodules.dggs_in_poly_for_geojson_callable import cells_in_poly
from auspixdggs.callablemodules.dggs_in_line import line_to_DGGS, densify_my_line
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
from pyproj import Transformer

rdggs = RHEALPixDGGS() # make an instance

def dggs_cell_id_to_obj(dggs_cell_id):
    #turn string into list first
    id_segments = list(dggs_cell_id)
    input_list = [id_segments.pop(0)]
    for s in id_segments:
        input_list.append(int(s))
    cell = rdggs.cell(input_list)
    return cell

def dggs_cell_id_list_to_obj(dggs_cell_id_list):
    res_list = []
    for item in dggs_cell_id_list:
        res_list.append(dggs_cell_id_to_obj(item))
    return res_list

def transform_coordinates(x, y, from_epsg, to_epsg):
    epsg_from = "epsg:{}".format(from_epsg)
    epsg_to = "epsg:{}".format(to_epsg)
    transformer = Transformer.from_crs(epsg_from, epsg_to, always_xy=True)
    return transformer.transform(x, y)


def latlong_to_DGGS(coords, resolution, from_epsg=None):
    '''
    This function takes coords (array of x and y) and returns the dggs cell ID at an input resolution.
    If from_epsg is set, then the coordinates are transformed to epsg:4326 or WGS84 (CRS that the DGGS engine expects)
    using pyproj with the always_xy parameter set to True. Otherwise, it assumes coords are in WGS84.
    '''
    coords_to_use = coords
    if from_epsg is not None:
        coords_to_use = transform_coordinates(coords[0], coords[1], from_epsg, 4326) #convert to epsg:4326 or WGS84
    # calculate the dggs cell from long and lat
    thisCell = rdggs.cell_from_point(resolution, coords_to_use, plane=False)  # false = on the elipsoidal curve
    # now have a dggs cell for that point
    return thisCell

def bbox(coord_list):
     box = []
     for i in (0,1):
         res = sorted(coord_list, key=lambda x:x[i])
         box.append((res[0][i],res[-1][i]))
     ret = [ box[0][0], box[1][0], box[0][1], box[1][1] ]
     return ret

def geojson_to_shape(g):
    return shape(g)

def get_cells_in_feature(fea, resolution, return_cell_obj=False):
    geom = geojson_to_shape(fea['geometry'])
    cells = []
    if isinstance(geom, Point) or isinstance(geom, MultiPoint): 
        # return cell object for Point or multiPoint
        curr_coords = list(coords(fea))
        for coord in curr_coords:
            cells.append(latlong_to_DGGS(coord, resolution))
    elif isinstance(geom, LineString) or isinstance(geom, MultiLineString): 
        # return cell object for line
        fea['geometry']['coordinates'] = densify_my_line(fea['geometry']['coordinates'], resolution)
        curr_coords = list(coords(fea))
        cells = line_to_DGGS(curr_coords, resolution)
    elif isinstance(geom, Polygon):
        curr_coords = list(coords(fea))
        thisbbox = bbox(curr_coords)
        res_cells = cells_in_poly(thisbbox, [fea['geometry']['coordinates']], resolution, return_cell_obj)  
        cells = [item[0] for item in res_cells]
    elif isinstance(geom, MultiPolygon):
        # return cell string
        curr_coords = list(coords(fea))
        thisbbox = bbox(curr_coords)
        res_cells = cells_in_poly(thisbbox, fea['geometry']['coordinates'], resolution, return_cell_obj)  
        cells = [item[0] for item in res_cells]

    return cells

def get_cells_in_geojson(geojson, resolution, return_cell_obj=False):
    list_cells = []
    for fea in geojson['features']:  # for feature in attribute table
        res_cells = get_cells_in_feature(fea, resolution, return_cell_obj)
        list_cells = list(list_cells + res_cells)
    return list_cells

def get_cells_with_property_in_geojson(geojson, resolution, return_cell_obj=False):
    list_cells = []
    list_property = []
    for fea in geojson['features']:  # for feature in attribute table
        res_cells = get_cells_in_feature(fea, resolution, return_cell_obj)
        list_cells.append(res_cells)
        list_property.append(fea['properties'])
    # print(list_cells)
    return list_cells, list_property

def reduce_duplicate_cells_2d_array(cells):
    # input 2-d array of cells
    # return original cells (str or object)
    unique_cells = []
    unique_cells_str = []
    for cell_array in cells:
        # 1-d array
        for cell in cell_array:
            cell_id = str(cell)
            if cell_id not in unique_cells_str:
                unique_cells_str.append(cell_id)
                unique_cells.append(cell)
    return unique_cells
    
def reduce_duplicate_cells_properties(cells, properties):
    # return original cells (str or object)
    unique_cells = []
    unique_cells_str = []
    unique_properties = []
    for i, cell_array in enumerate(cells):
        for cell in cell_array:
            cell_id = str(cell)
            if cell_id not in unique_cells_str:
                unique_cells_str.append(cell_id)
                unique_properties.append(properties[i])
                unique_cells.append(cell)
    return unique_cells, unique_properties