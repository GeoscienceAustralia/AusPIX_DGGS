# AusPIX
AusPIX is an Australian Government implimentation of the rHealpix DGGS. 

AusPIX specifies the starting points of the rHealpix top-level cells to achineve some Australian aims, such as including most of the Australian continent within once cell.

This repository contains the rHealPIX "engine" and a series of scripts that use AusPIX in a variety of ways.
There are several 'callable' modules that perform common tasks in DGGS space. These are in the "callable_modules" folder.


## Grid Imagery
The following images show the structure and positioning of the AusPIX grid relative to the earth's globe.

![rhealpix](https://user-images.githubusercontent.com/23160509/53066271-23aa4680-3523-11e9-8e6c-2f042f9befbf.png)  
Figure 1: World Grid layout.

![maindggsregions](https://user-images.githubusercontent.com/23160509/53380635-35c43300-39c2-11e9-90ea-e457d03b8726.png)  
Figure 2: Major AusPIX divisions in the Australian region.

![auspixlevel10](https://user-images.githubusercontent.com/23160509/53381199-1cbc8180-39c4-11e9-86d2-8a7a12b50faf.png)  
Figure 3:  Sample AusPIX level 10 cells (approx 140 x 140 m) near the lake in Canberra.


 
## Installation 

`python setup.py install`  
or   
`pip install .`   
or for development  
`python setup.py develop`  
or   
`pip install -e .`

### Running tests

``` 
$ pip install pytests
$ python -m pytests tests/
```


## Development History

Wrapper scripts developed by Bell, J.G. at Geoscience Australia are catalogued with the follwing Geoscience eCat record: 
* <http://pid.geoscience.gov.au/dataset/ga/140148>

Some speed enhancements by CSIRO under contract, Funded by the Australian Government [Location Index Project](https://www.ga.gov.au/locationindex).

Initial guidance by Matt Purss, formerly based at Geosciece Australia.

rHealPIX DGGS engine developed by Gibb, R.G _et al._

Source references for rHealPIX:

* Gibb, R.G. (2016) "The rHealPIX Discrete Global Grid System" Proceedings of the 9th Symposium of the International Society for Digital Earth (ISDE), Halifax, Nova Scotia, Canada. IOP Conf. Series: Earth and Environmental Science, 34, 012012. DOI: [10.1088/1755-1315/34/1/012012](https://doi.org/10.1088/1755-1315/34/1/012012)
* Gibb R G, Raichev A and Speth M (2013) "The rHEALPix Discrete Global Grid System" DOI: [10.7931/J2D21VHM](https://doi.org/10.7931/J2D21VHM).


## License & Rights

Software in this repository is licensed for use under the [Apache 2.0 Software License](), a copy of the deed of which is contained in the [LICENSE](LICENSE) file.

This work is copyright: &copy; Australian Government (Geosicence Australia), 2020.


## Citation
Please cite this work with the following BibTex description:

```bibtex
@software{AusPIX_DGGS,
  title = {{AusPIX: An Australian Government implimentation of the rHealpix DGGS in Python}},
  date = {2020},
  publisher = "Geoscience Australia",
  url = {https://github.com/GeoscienceAustralia/AusPIX_DGGS}
}
```

## Contact

**Joseph G. Bell**  
_Geospatial Data Scientist_  
National Land Information,  
Geosciece Australia  
<joseph.bell@ga.gov.au>
