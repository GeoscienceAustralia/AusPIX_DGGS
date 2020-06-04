from ..auspixengine.dggs import RHEALPixDGGS
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
