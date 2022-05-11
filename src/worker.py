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
    
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Intensity of Wind Speed in Texas and Oklahoma")

    time.sleep(15) # Lol definitely gonna need to replace this
    update_job_status(jid, 'complete')

execute_job()
