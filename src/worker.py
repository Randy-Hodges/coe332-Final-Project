from jobs import q, update_job_status, rd, jdb, img_db
import time
import matplotlib.pyplot as plt
import numpy as np
from hotqueue import HotQueue
import json
import os
import redis

@q.worker
def execute_job(jid):
    """ Executes a wind analysis job.
    
    Arguments:
        jid (str): job id for the job to be performed.

    Returns:
        None. This function continuously runs in the background.
    
    """
    update_job_status(jid, 'in progress')
    
    data = jdb.hgetall(f'job.{jid}')
    stored_data = json.loads(rd.get("data"))
    stored_data = stored_data[f'{data["LAT"]}, {data["LON"]}, {data["PARAMETER"]}, {data["YEAR"]}']
    xval = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    yval = []

    for month in xval:
        yval.append(float(stored_data[month]))

    plt.xlabel("Months")
    plt.ylabel("Wind Speed")
    plt.title(f'Wind Speed in {data["YEAR"]} at Lat = {data["LAT"]} and Lon = {data["LON"]}')
    plt.plot(xval, yval)
    plt.savefig('/simple_line.png')

    with open('/simple_line.png', 'rb') as f:
        img = f.read()

    img_db.hset(f'job.{jid}', "image", img)

    jdb.hset(f'job.{jid}', 'status', 'finished')
    update_job_status(jid, 'finished')

    time.sleep(2) 
    update_job_status(jid, 'complete')


execute_job()
