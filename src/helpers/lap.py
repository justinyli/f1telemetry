import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

# Load the telemetry data
fastf1.Cache.enable_cache('cache')
fastf1.plotting.setup_mpl()

# Session 1 details
year1 = 2023
event1 = 'British'
session1_name = 'R'
driver1_name = 'NOR'

# Session 2 details
year2 = 2023
event2 = 'British'
session2_name = 'R'
driver2_name = 'VER'

drivers = [driver1_name, driver2_name]

# Fetch session data
session1 = fastf1.get_session(year1, event1, session1_name)
session2 = fastf1.get_session(year2, event2, session2_name)

# Load session data
session1.load()
session2.load()

lap = 23

# Pick drivers
driver1 = session1.laps.pick_driver(driver1_name)
driver2 = session2.laps.pick_driver(driver2_name)

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
axs[0].set_title(drivers[0] + ' (' + str(year1) + ', ' + session1_name + ') vs. ' + drivers[1] + ' (' + str(year2) + ', ' + session2_name + ')' )
for ax in axs:
    ax.legend()

# Adjust subplot spacing
plt.subplots_adjust(left=0.04, bottom=0.038, right=0.99, top=0.95, wspace=0.2, hspace=0.1)

# Display the plot
plt.savefig('static/img/lap.png', transparent = False, bbox_inches='tight', dpi = 200)