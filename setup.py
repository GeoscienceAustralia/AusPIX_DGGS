from setuptools import setup, find_packages

setup(
    name='auspixdggs',
    version='1.0.0',
    url='https://github.com/GeoscienceAustralia/AusPIX_DGGS',
    author='Joseph Bell',
    author_email='Joseph.Bell@ga.gov.au',
    description='This is the base python DGGS engine for the AusPIX developmental DGGS by Geoscience Australia.',
    packages=find_packages(),    
    install_requires=['numpy', 'pyproj', 'scipy', 'shapely'],
)
