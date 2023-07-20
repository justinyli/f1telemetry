import fastf1 as ff1
from fastf1 import plotting
from fastf1.livetiming.data import LiveTimingData
import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
import pyqtgraph as pg

matplotlib.use('TkAgg')
plotting.setup_mpl()

ff1.Cache.enable_cache('cache\\live', force_renew=True) 
livedata = LiveTimingData('cache\\live\\saved_data.txt') #can add a second one
#python -m fastf1.livetiming save D:\F1live\saved_data.txt

session = ff1.get_session(2023, 'Hungarian', 'FP1')
session.load()

lap = 23

driver1_name = 'VER'
driver2_name = 'NOR'

drivers = [driver1_name, driver2_name]

lap = 23

# Pick drivers
driver1 = session.laps.pick_driver(driver1_name)
driver2 = session.laps.pick_driver(driver2_name)

# Fetch telemetry data
driver1_telemetry = driver1[driver1['LapNumber'] == lap].iloc[0].get_telemetry()
driver2_telemetry = driver2[driver2['LapNumber'] == lap].iloc[0].get_telemetry()

# Add distance information
driver1_telemetry = driver1_telemetry.add_distance()
driver2_telemetry = driver2_telemetry.add_distance()

# Telemetry attributes
telemetry_attributes = ['Speed', 'Brake', 'Throttle', 'nGear', 'RPM']
colors = ['red', 'blue']

# Create subplots
plt.clf()
fig, axs = plt.subplots(len(telemetry_attributes), sharex=True)

# Plot telemetry data
for i, attribute in enumerate(telemetry_attributes):
    for j, driver_telemetry in enumerate([driver1_telemetry, driver2_telemetry]):
        axs[i].plot(driver_telemetry['Distance'], driver_telemetry[attribute], label = drivers[j], color=colors[j], alpha=0.5)
    axs[i].set_ylabel(attribute)

# Set title and legends
axs[0].set_title(drivers[0] + ' vs. ' + drivers[1])
for ax in axs:
    ax.legend()

# Adjust subplot spacing
plt.subplots_adjust(left=0.04, bottom=0.038, right=0.99, top=0.95, wspace=0.2, hspace=0.1)

# Display the plot
plt.savefig('static/img/lap.png', transparent = False, bbox_inches='tight', dpi = 200)