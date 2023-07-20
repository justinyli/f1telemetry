import fastf1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the telemetry data
fastf1.Cache.enable_cache("cache")  # Optional: Enable caching for faster data retrieval
session = fastf1.get_session(2023, 'British', 'R')

# FF1 3.0.0
session.load()

lap = 23

driver = session.laps.pick_driver('NOR')
driver_telemetry = driver[driver['LapNumber'] == lap].iloc[0].get_telemetry()
x = driver_telemetry['X']
y = driver_telemetry['Y']
speed = driver_telemetry['Speed']


bins = 100
H, xedges, yedges = np.histogram2d(x, y, bins = bins, weights = speed)
H_counts, xedges, yedges = np.histogram2d(x, y, bins = bins) 
for i in range(len(H_counts)):
    for j in range(len(H_counts[0])):
        if H_counts[i][j] == 0:
            H_counts[i][j] = 1
H = H/H_counts

extent = extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.imshow(H.T, origin='lower',  cmap='magma', extent = extent)            
plt.title('Telemetry Heatmap - Speed')
plt.colorbar()
plt.axis('off')
plt.savefig('static/img/heatmap.png', transparent = False, bbox_inches='tight', dpi = 600)