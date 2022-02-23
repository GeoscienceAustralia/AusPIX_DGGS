# AusPIX
AusPIX is an Australian Government implimentation of the rHealpix DGGS. 

AusPIX specifies the starting points of the rHEALPix top-level cells to achineve some Australian aims, such as including most of the Australian continent within once cell.

This repository contains the rHealPIX "engine" and a series of scripts that use AusPIX in a variety of ways.
There are several 'callable' modules that perform common tasks in DGGS space. These are in the "callable_modules" folder.

# AusPIX Framework for cross-referencing spatial data
The AusPIX Framework is a system to spatially link geographical data for statistical cross-referencing. Point, line, polygon and raster data are referenced to DGGS cells to provide consistent and repeatable numbers. Any data that can be linked to a geography can be included, for example economic data collected on mesh-block or other ASGS series can be included. Environmental data collected as a raster can similarly be consumed and cross-referenced. 

Document:
https://ecat.ga.gov.au/geonetwork/srv/eng/catalog.search#/metadata/140152

Search eCat for "AusPIX" to find other resources including descriptive videos.

Example data-at-point query:
https://olpk7700l6.execute-api.ap-southeast-2.amazonaws.com/dataDrill?lat84=-35.34385&long84=149.15772
This query samples the data at that XY coordinate, suitable for automated machine interaction. 
Human readable format will be similar but with a map for the user to select the point they are interested in. (NB. only works during Canberra Business hours)
This tool lists all the geographies available in these 2 cross-walk tables.

Example of an area-query, here we are asking for Water observations from Space breakdown for an ASGS single SA1 polygon feature:
https://978uy7zro7.execute-api.ap-southeast-2.amazonaws.com/get?geography=sa1_main16&feature=11001118710&compareWith=wofs
Any data that is in the system can be cross-reference equally as easily.

# DGGS usage
DGGS tools can be used for many things. Here we have used DGGS to build and interact as an intelligent raster grid. This DGGS 'engine' is written in Python and supplies the grid at hierarchical levels, along with a set of functions for doing common tasks. DGGS provides a consistent and repeatable definition of a location as per the Loc-I concept.
The code is now at https://pypi.org/project/rHEALPixDGGS/  for anyone to download and use. Other python algorithems have been developed for the AusPIX framework to build usable components and outputs.

# DGGS Grid Imagery
The following images show the structure and positioning of the AusPIX grid relative to the earth's globe.

![rhealpix](https://user-images.githubusercontent.com/23160509/53066271-23aa4680-3523-11e9-8e6c-2f042f9befbf.png)  
Figure 1: World Grid layout.

![maindggsregions](https://user-images.githubusercontent.com/23160509/53380635-35c43300-39c2-11e9-90ea-e457d03b8726.png)  
Figure 2: Major AusPIX divisions in the Australian region.

![auspixlevel10](https://user-images.githubusercontent.com/23160509/53381199-1cbc8180-39c4-11e9-86d2-8a7a12b50faf.png)  
Figure 3:  Sample AusPIX level 10 cells (approx 140 x 140 m) near the lake in Canberra.


 
### Installation 

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


### Development History

Wrapper scripts developed by Bell, J.G. at Geoscience Australia are catalogued with the follwing Geoscience eCat record: 
* <http://pid.geoscience.gov.au/dataset/ga/140148>

Some speed enhancements by CSIRO under contract, Funded by the Australian Government [Location Index Project](https://www.ga.gov.au/locationindex).

Initial guidance by Matt Purss, formerly based at Geosciece Australia.

rHEALPix DGGS engine developed by Gibb, R.G _et al._

Source references for rHEALPix:

* Gibb, R.G. (2016) "The rHEALPix Discrete Global Grid System" Proceedings of the 9th Symposium of the International Society for Digital Earth (ISDE), Halifax, Nova Scotia, Canada. IOP Conf. Series: Earth and Environmental Science, 34, 012012. DOI: [10.1088/1755-1315/34/1/012012](https://doi.org/10.1088/1755-1315/34/1/012012)
* Gibb R G, Raichev A and Speth M (2013) "The rHEALPix Discrete Global Grid System" DOI: [10.7931/J2D21VHM](https://doi.org/10.7931/J2D21VHM).


### License & Rights

Software in this repository is licensed for use under the [Apache 2.0 Software License](), a copy of the deed of which is contained in the [LICENSE](LICENSE) file.

This work is copyright: &copy; Australian Government (Geosicence Australia), 2020.


### Citation
Please cite this work with the following BibTex description:

```bibtex
@software{AusPIX_DGGS,
  title = {{AusPIX: An Australian Government implimentation of the rHEALPix DGGS in Python}},
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
