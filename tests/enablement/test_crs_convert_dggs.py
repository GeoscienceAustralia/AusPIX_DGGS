from auspixdggs.callablemodules.dggs_for_points_geojson_callable import latlong_to_DGGS
from pyproj import Transformer
import pytest

def test_transform_3577_to_4326():
   x = 1549652.93
   y = -3960378.34
   answer = latlong_to_DGGS([x,y], 7, from_epsg=3577)
   print(answer)
   assert str(answer) == "R7852372"

if __name__ == "__main__":
   test_transform_3577_to_4326()
