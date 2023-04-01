import folium
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.signal import savgol_filter
from wtss import *

service = WTSS('https://brazildatacube.dpi.inpe.br/',
               access_token='rfFSFltuVwZg98aqcrx06einGOvf1OAhC2FMc2dXT9'
               )

service.coverages

coverage = service['CB4_64_16D_STK-1']

timeline = coverage.timeline
start = timeline[0]
end = timeline[-1]

print(f'Interval range: [{start}, {end}]')

ts = coverage.ts(attributes=('BAND15', 'BAND16'),
                 latitude=-12.0,
                 longitude=-54.0,
                 start_date='2016-01-01',
                 end_date='2016-12-31'
                 )
ts.BAND15
ts.BAND16
ts.plot()

cb4_timeseries_cmask = coverage.ts(
    attributes=('CMASK'),
    latitude=-12.0,
    longitude=-53.989,
    start_date='2017-01-01',
    end_date='2019-12-31'
)
set(cb4_timeseries_cmask.values('CMASK'))

cb4_timeseries = coverage.ts(
    attributes=('NDVI', 'CMASK'),
    latitude=-12.0,
    longitude=-53.989,
    start_date='2017-01-01',
    end_date='2019-12-31'
)

ndvi_timeline = pd.to_datetime(cb4_timeseries.timeline)
ndvi_data = np.array(cb4_timeseries.NDVI)
cmask_data = np.array(cb4_timeseries.CMASK)

cmask_data = np.where(cmask_data == 255, np.nan, 1)

ndvi_data * cmask_data

ndvi_masked_data = pd.DataFrame(
    {'data': ndvi_data * cmask_data}, index=pd.to_datetime(ndvi_timeline))
ndvi_masked_data[ndvi_masked_data['data'].isna()]

ndvi_masked_data_interpolated = ndvi_masked_data.interpolate()
ndvi_masked_data_interpolated[ndvi_masked_data_interpolated['data'].isna()]

plt.figure(dpi=120)
plt.plot(ndvi_data, color='gray', linestyle='dashed', label='Original')
plt.plot(
    ndvi_masked_data_interpolated['data'].values, color='blue', label='Interpolada')
plt.title('Comparação de série temporal com e sem interpolação')
plt.legend()
plt.grid(True)
plt.show()

median_smoothed = savgol_filter(
    ndvi_masked_data_interpolated['data'], window_length=9, polyorder=2)

plt.figure(dpi=120)
plt.plot(ndvi_masked_data_interpolated['data'].values,
         color='gray', linestyle='dashed', label='Interpolada')
plt.plot(median_smoothed, color='blue', label='Interpolada e suavizada')
plt.title('Comparação de série temporal com e sem suavização')
plt.legend()
plt.grid(True)
plt.show()

longitude = -53.989
locations = []

for latitude in np.arange(-16.9000, -16.9075, -0.0015):
      locations.append((latitude, longitude))

m = folium.Map(
      location = [-16.9, -53.989],
      zoom_start = 15
)

tile = folium.TileLayer(
      tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{}',
      attr = 'Esri',
      name = 'Esri Satellite',
      overlay = False,
      control = True
).add_to(m)

for location in locations:
      folium.Cicrle(
            fill=True,
            color = 'orange',
            location=location
      ).add_to(m)

adriculture_time_series = []

for location in locations:
      latitude, longitude = location
      time_series = coverage.ts(
            attributes=('NDVI'),
            latitude=float(latitude),
            longitude=float(longitude),
            start_date='2017-01-01',
            end_date='2019-12-31'
      )

adriculture_time_series.append(time_series.values('NDVI'))

median = np.median(adriculture_time_series, axis = 0)

plt.figure(dpi=120)
for i in range(len(adriculture_time_series)):
      plt.plot(adriculture_time_series[i], color='gray', alpha = .2)
plt.plot(median, color='blue', linewidth=1)
plt.grid(True)
plt.show()