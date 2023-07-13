import fastf1
import matplotlib.pyplot as plt
import pandas as pd

# Load the telemetry data
fastf1.Cache.enable_cache("D:\\F1")  # Optional: Enable caching for faster data retrieval
session = fastf1.get_session(2023, 'British', 'R')

# FF1 3.0.0
session.load()

driver_telemetry = session.laps.pick_driver('NOR').pick_fastest().get_telemetry()
x = driver_telemetry['X']
y = driver_telemetry['Y']
speed = driver_telemetry['Speed']

# Create the heatmap
fig, ax = plt.subplots()
heatmap = ax.hist2d(x, y, bins=50, weights=speed, cmap='hot')

# Add colorbar
cbar = plt.colorbar(heatmap[3], ax=ax)
cbar.set_label('Speed (km/h)')

# Set the x and y axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Add title to the plot
ax.set_title('Telemetry Heatmap - Speed')

# Show the plot
plt.show()