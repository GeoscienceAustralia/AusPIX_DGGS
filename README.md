# AusPIX_DGGS
The AusPIX DGGS is an Australian Government implimentation of the rHealpix DGGS model.

Included in this repository is the rHealPIX "engine" and a series of scripts that use AusPIX in a variety of ways.

Additionally there are several 'callable' modules that perform common tasks in DGGS space. These are in the "callable_modules" folder.
## Installation 

`python setup.py install`  
or   
`pip install .`   
or for development  
`python setup.py develop`  
or   
`pip install -e .`

## Running tests

``` 
$ pip install pytests
$ python -m pytests tests/
```

![rhealpix](https://user-images.githubusercontent.com/23160509/53066271-23aa4680-3523-11e9-8e6c-2f042f9befbf.png)
Figure 1: World Grid layout:

![maindggsregions](https://user-images.githubusercontent.com/23160509/53380635-35c43300-39c2-11e9-90ea-e457d03b8726.png)

Figure 2: Major AusPIX divisions in the Australian region.

![auspixlevel10](https://user-images.githubusercontent.com/23160509/53381199-1cbc8180-39c4-11e9-86d2-8a7a12b50faf.png)

Figure 3:  Sample AusPIX level 10 cells (approx 140 x 140 m) near the lake in Canberra.

Source references for rHealPIX:

Gibb, R.G., 2016, “The rHealPIX Discrete Global Grid System” Proceedings of the 9th Symposium of the International Society for Digital Earth (ISDE), Halifax, Nova Scotia, Canada. IOP Conf. Series: Earth and Environmental Science, 34, 012012. DOI: 10.1088/1755-1315/34/1/012012

Gibb R G, Raichev A and Speth M 2013 The rHEALPix Discrete Global Grid System URL http://dx.doi.org/10.7931/J2D21VHM

 



