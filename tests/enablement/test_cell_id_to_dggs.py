import pytest
from auspixdggs.callablemodules.util import dggs_cell_id_to_obj


def test_cell_id_to_cell_obj():
    # read in the file
    c = dggs_cell_id_to_obj('R7751215231')
    print(c)
    verts = c.vertices(plane=False)
    vertices = [(138.75323883554336, -34.710999884272056), (138.75476299344612, -34.710999884272056), (138.75476299344612, -34.712573832391016), (138.75323883554336, -34.712573832391016)]
    assert verts == vertices
    
if __name__ == "__main__":
    test_cell_id_to_cell_obj()