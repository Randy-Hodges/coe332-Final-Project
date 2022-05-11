from jobs import q, update_job_status
import time
import matplotlib.pyplot as plt
import numpy as np
from hotqueue import HotQueue
import json
import os
import redis

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')
    """
    Current Plan: Heat Map of wind speeds (use ANN)
    Other Options: basic graph/scatter plot of wind speeds throughout the years/months 
    in a specific (lat, long)
    """
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Intensity of Wind Speed in Texas and Oklahoma")

    time.sleep(15) # Lol definitely gonna need to replace this
    update_job_status(jid, 'complete')

execute_job()
