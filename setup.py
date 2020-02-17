from setuptools import setup, find_packages

setup(
    name='AusPIXengine',
    version='1.0.0',
    url='',
    author='',
    author_email='',
    description='This is the base python DGGS engine for the AusPIX developmental DGGS by Geoscience Australia.',
    packages=find_packages(),    
    install_requires=['numpy', 'pyproj', 'scipy'],
)
