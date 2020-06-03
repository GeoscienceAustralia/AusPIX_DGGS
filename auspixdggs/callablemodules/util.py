from ..auspixengine.dggs import RHEALPixDGGS
rdggs = RHEALPixDGGS() # make an instance

def dggs_cell_id_to_obj(dggs_cell_id):
    #turn string into list first
    id_segments = list(dggs_cell_id)
    input_list = [id_segments.pop(0)]
    for s in id_segments:
        input_list.append(int(s))
    cell = rdggs.cell(input_list)
    return cell