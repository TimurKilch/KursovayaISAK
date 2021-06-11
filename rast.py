import rasterio
from rasterio import plot
import numpy

def ndvi_caclucate_landsat7(img_b3,img_b4):
    band_red = rasterio.open(img_b3)
    band_nir = rasterio.open(img_b4)
    red = band_red.read(1).astype('float64')
    nir = band_nir.read(1).astype('float64')
    ndvi = numpy.where((nir+red)==0.,0,(nir-red)/(nir+red))
    return ndvi;
