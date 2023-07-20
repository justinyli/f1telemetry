from flask import Flask, render_template, request
import fastf1 as ff1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

app = Flask(__name__)
ff1.Cache.enable_cache('D:\\F1')
plotting.setup_mpl()

@app.route('/')
def index():
    return render_template('index.html')

def graph_heatmap(year, event, session, driver, lap):
    ff1.Cache.enable_cache("cache")  # Optional: Enable caching for faster data retrieval
    session = ff1.get_session(year, event, session)
    
    session.load()
        
    driver = session.laps.pick_driver(driver)
    
    if lap == "F":
        driver_lap = driver.pick_fastest()
    else:
        driver_lap = driver[driver['LapNumber'] == lap].iloc[0]
    driver_telemetry = driver_lap.get_telemetry()
    
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
    H = H / H_counts
    
    extent = extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.clf()
    plt.imshow(H.T, origin='lower',  cmap='magma', extent = extent)            
    plt.title('Telemetry Heatmap - Speed')
    plt.colorbar()
    plt.axis('off')
    plt.savefig('static/img/heatmap.png', transparent = False, bbox_inches='tight', dpi = 200)
    
    return True

def graph_tel(year1, event1, session1_name, driver1, lap1, year2, event2, session2_name, driver2, lap2):
    ff1.Cache.enable_cache('cache')
    ff1.plotting.setup_mpl()
    drivers = [driver1, driver2]
    
    session1 = ff1.get_session(year1, event1, session1_name)
    session2 = ff1.get_session(year2, event2, session2_name)
    
    session1.load()
    session2.load()
    
    driver1 = session1.laps.pick_driver(driver1)
    driver2 = session2.laps.pick_driver(driver2)
    
    if lap1 == "F":
        driver1_lap = driver1.pick_fastest()
    else:
        driver1_lap = driver1[driver1['LapNumber'] == lap].iloc[0]
    
    if lap2 == "F":
        driver2_lap = driver2.pick_fastest()
    else:
        driver2_lap = driver2[driver2['LapNumber'] == lap].iloc[0]
    
    driver1_telemetry = driver1_lap.get_telemetry()
    driver2_telemetry = driver2_lap.get_telemetry()
    
    telemetry_attributes = ['Speed', 'Brake', 'Throttle', 'nGear', 'RPM']
    colors = ['red', 'blue']
    
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
    
    return True


@app.route('/heatmap', methods=['GET', 'POST'])
def heat_maps():
    if request.method == 'POST':
        year = int(request.form['year'])
        event = request.form['event']
        session = request.form['session']
        driver = request.form['driver']
        lap = request.form['lap']
        
        bool_img = graph_heatmap(year, event, session, driver, lap)
        
        return render_template('heatmap.html', image = bool_img)
    else:
        return render_template('heatmap.html')
    

@app.route('/lap', methods = ['GET', 'POST'])
def lap():
    if request.method == 'POST':
        year1 = int(request.form['year1'])
        event1 = request.form['event1']
        session1 = request.form['session1']
        driver1 = request.form['driver1']
        lap1 = request.form['lap1']
        
        year2 = int(request.form['year2'])
        event2 = request.form['event2']
        session2 = request.form['session2']
        driver2 = request.form['driver2']
        lap2 = request.form['lap2']
        
        bool_img = graph_tel(year1, event1, session1, driver1, lap1, year2, event2, session2, driver2, lap2)
        
        return render_template('lap.html', image = bool_img)
    else:
        return render_template('lap.html')

if __name__ == "__main__":
    app.run(debug = True)