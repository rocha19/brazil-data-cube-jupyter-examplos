import folium
import matplotlib.pyplot as plt
import numpy
import pandas as pd
import plotly.express as px
import scipy

from wtss import WTSS

w = WTSS('http://www.esensing.dpi.inpe.br/')
service = WTSS('https://brazildatacube.dpi.inpe.br/',
               access_token='rfFSFltuVwZg98aqcrx06einGOvf1OAhC2FMc2dXT9'
               )

ts = w.time_series(coverage='MOD13Q1', attributes=('red', 'nir'),
                   latitude=-12.0, longitude=-54.0,
                   start_date='2001-01-01', end_date='2001-12-31')

fig, ax = plt.subplots()

plt.title('Time Series MOD13Q1', fontsize=24)

plt.xlabel('Date', fontsize=16)
plt.ylabel('Surface Reflectance', fontsize=16)

ax.plot(ts.timeline, ts['red'], color='red', ls='-', marker='o', label='red')
ax.plot(ts.timeline, ts['nir'], color='purple',
        ls='-', marker='o', label='nir')

plt.legend()

plt.grid(b=True, color='gray', linestyle='--', linewidth=0.5)

fig.autofmt_xdate()

plt.show()
