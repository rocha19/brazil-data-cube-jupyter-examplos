import stac
from rasterio.windows import Window
from matplotlib import pyplot as plt
import numpy

# import os
# del os.environ['PROJ_LIB']

stac.__version__

service = stac.STAC('https://brazildatacube.dpi.inpe.br/stac/',
                    access_token='rfFSFltuVwZg98aqcrx06einGOvf1OAhC2FMc2dXT9')

collection = service.collection('CB4_64_16D_STK-1')

getItems = collection.get_items(
	filter={
		'bbox': '-46.62597656250001, -13.19716452328198, -45.03570556640626, -12.297068292853805',
		'datetime': '2018-08-01/2029-07-31',
		'limit': 10
    }
)

for item in getItems:
	item.id

item = getItems.features[2]

assets = item.assets

for k in assets.keys():
    k

blueAsset = assets['BAND13']

for asset in assets.values():
    asset

nir = item.read('BAND15')

red = item.read('BAND15', window=Window(0, 0, 500, 500)) # Window(col_off, row_off, width, height)

green = item.read('BAND14', window=Window(0, 0, 500, 500))

blue = item.read('BAND13', window=Window(0, 0, 500, 500))

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
ax1.imshow(red, cmap='gray')
ax2.imshow(green, cmap='gray')
ax3.imshow(blue, cmap='gray')

def normalize(array):
  array_min, array_max = array.min(), array.max()
  return ((array - array_min) / (array_max - array_min))

rgb = numpy.dstack((normalize(red), normalize(green), normalize(blue)))

plt.imshow(rgb)

blueAsset.download('img')

item.download('images')

blueAsset.href
