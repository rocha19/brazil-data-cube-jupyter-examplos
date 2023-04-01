import folium
import matplotlib.pylab as plt
import numpy
import pandas as pd
import plotly.express as px
from scipy.signal import savgol_filter

from wtss import WTSS

service = WTSS('https://brazildatacube.dpi.inpe.br/',
               access_token='rfFSFltuVwZg98aqcrx06einGOvf1OAhC2FMc2dXT9'
               )

cbers4Coverage = service['CB4_64_16D_STK-1']

redBand = 'BAND15'
nirBand = 'BAND16'

timeSeries = cbers4Coverage.ts(
    attributes=(redBand, nirBand),
    latitude=-16.817,
    longitude=-52.079,
    start_date='2017-01-01',
    end_date='2019-12-31'
)

timeSeries.plot()

plt.scatter(timeSeries.values(redBand), timeSeries.values(nirBand), alpha=0.5)
plt.title('Scatter plot')
plt.xlabel('Red')
plt.ylabel('NIR')
plt.show()

timeSeries2 = cbers4Coverage.ts(
    attributes=(redBand, nirBand),
    latitude=-16.819,
    longitude=-52.079,
    start_date='2017-01-01',
    end_date='2019-12-31'
)

plt.scatter(timeSeries.values(nirBand), timeSeries2.values(nirBand), alpha=0.5)
ident = [0.0, max(timeSeries.values(nirBand))]
plt.plot(ident, ident, color='red', ls='--')
plt.title('Scatter plot')
plt.xlabel('NIR TS1')
plt.ylabel('NIR TS2')
plt.show()

agricultureTimeSeries = []
for latitude in numpy.arange(-16.905, -16.955, -0.01):
    timeSeries = cbers4Coverage.ts(
        attributes=(nirBand),
        latitude=float(latitude),
        longitude=-53.989,
        start_date='2017-01-01',
        end_date='2019-12-31'
    )
    agricultureTimeSeries.append(timeSeries.values(nirBand))
e
median = numpy.median(agricultureTimeSeries, axis=0)

for i in range(len(agricultureTimeSeries)):
    plt.plot(agricultureTimeSeries[i], color='grey', alpha=0.5)
plt.plot(median, color='blue', linewidth=2)
plt.show()

madianSmoothed = savgol_filter(median, windowLength=9, polyorder=2)

plt.plot(median, color='blue')
plt.plot(madianSmoothed, color='red')
plt.show()

m = folium.Map(location=[-9.92, -51.37], zoom_start=4)

ymin = cbers4Coverage.spatial_extent['ymin']
ymax = cbers4Coverage.spatial_extent['ymax']

xmin = cbers4Coverage.spatial_extent['xmin']
xmax = cbers4Coverage.spatial_extent['xmax']

folium.Rectangle(bounds=[(ymin, ymax), (xmin, xmax)], color='#ff7800',
                 fill=True, fill_color='#ffff00', fill_opacity=0.2).add_to(m)

cbersDF = pd.DataFrame({'BAND15': timeSeries.BAND15, 'BAND16': timeSeries.BAND16},
                       index=pd.to_datetime(timeSeries.timeline))

fig = px.line(cbersDF, x=cbersDF.index, y=['BAND15', 'BAND16'], title='CBERS-4/AWFI (BRAND 15 and BAND 16)', 'index': 'Date', 'value': 'Spectral Reflexctance (scaled)')
fig.update_xaxes(rangeslider_visible=True)
fig.show()

