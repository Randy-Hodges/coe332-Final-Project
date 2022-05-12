from jobs import q, update_job_status, rd, jdb, img_db
import time
import matplotlib.pyplot as plt
import numpy as np
"""
import seaborn as sns     May want to use this bc of the color bar legend thing, unsure about how the list of lists need to be organized for the heatmap
                          outputting methods tbh

NOTE: Still have not tested to see if this works (honestly not sure how to)
"""
from hotqueue import HotQueue
import json
import os
import redis

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    
    data = jdb.hgetall(f'job.{jid}')
    xval = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    yval = []

    for month in xval:
        yval.append(data[month])

    plt.xlabel("Months")
    plt.ylabel("Wind Speed")
    plt.title(f'Wind Speed in {data["YEAR"]} at Lat = {data["LAT"]} and Lon = {data["LON"]}')
    plt.plot(xval, yval, 'b-')
    plt.savefig('/simple_line.png')

    with open('/simple_line.png', 'rb') as f:
        img = f.read()

    img_db.hset(jid, img)



    # data = []
    # lat = []
    # lon = []
    # spd_data = []
    # for key in rd.keys()
    #     if float(json.loads(rd.get(key))['YEAR']) == 2010 and json.loads(rd.get(key))['PARAMETER'] == 'WS50M':  #maybe want to allow some kind of user input or wtv to specify a year
    #         data.append(json.loads(rd.get(key)))
    #         lat.append(float(json.loads(rd.get(key))['LAT']))
    #         lon.append(float(json.loads(rd.get(key))['LON']))
    #         lon = list(set(sorted(lon)))
    #         lat = list(set(sorted(lat, reverse=True)))
    # for i in lat:
    #     row = [] 
    #     for j in lon:
    #         for item in data:
    #             if float(json.loads(rd.get(key))['LAT']) == i and float(json.loads(rd.get(key))['LON']) == j:
    #                 row.append(float(json.loads(rd.get(key))['ANN']))
    #                 break
    #     spd_data.append(row)

    # plt.axis([-103.25, -93.75, 27.25, 36.75])
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    # plt.title("Intensity of Wind Speed in Texas and Oklahoma")
    # plt.imshow(spd_data, cmap = 'summer', interpolation = 'nearest')
    # plt.savefig('/windspeed_data_output.png')
    
    time.sleep(2) 
    update_job_status(jid, 'complete')


execute_job()
