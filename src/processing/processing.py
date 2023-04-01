import stac
from matplotlib import pyplot as plt

service = stac.STAC('https://brazildatacube.dpi.inpe.br/stac/',
                    access_token='rfFSFltuVwZg98aqcrx06einGOvf1OAhC2FMc2dXT9')

bbox = (-45.9, -12.9, -45.4, -12.6)

items = service.search({
	'collections': ['CB4_64_16D_STK-1'],
	'bbox': bbox,
	'datetime': '2018-08-01/2019-07-31',
	'limit': 30
})

len(items.features)

item = items.features[0]

red = item.read('BAND15', bbox=bbox)

nir = item.read('BAND16', bbox=bbox)

plt.imshow(red, cmap='gray')

plt.imshow(nir, cmap='gray')

ndvi = (nir - red) / (nir + red)

plt.imshow(ndvi, cmap='gray') # Quanto mais claro tem mais vegetação

plt.imshow(ndvi, cmap='jet')

plt.title('NDVI Histogram')
plt.hist(ndvi)
plt.show()

labeledImg = ndvi.copy()
labeledImg[ndvi < 0.2] = 1
labeledImg[ndvi >= 0.2] = 3
labeledImg[ndvi >= 0.45] = 2

plt.rcParams['figure.figsize'] = [30, 20]
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(ndvi, cmap='gray')
ax2.imshow(labeledImg, cmap='brg')

firstItem = items.features[0]

ndviFirstImage = firstItem.read('NDVI', bbox=bbox)

secondItem = items.features[13]

ndviSecondImage = secondItem.read('NDVI', bbox=bbox)

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(ndviFirstImage, cmap='gray')
ax2.imshow(ndviSecondImage, cmap='gray')

ndviDiff = ndviFirstImage - ndviSecondImage
plt.rcParams['figure.figsize'] = [10, 5]
plt.imshow(ndviDiff, cmap='jet')
