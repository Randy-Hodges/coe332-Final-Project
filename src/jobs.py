import json
import os
import uuid
from flask import Flask, request
import redis
from hotqueue import HotQueue


redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception("no redis ip")

rd = redis.Redis(host=redis_ip, port=6379, db=0)
q = HotQueue("queue", host=redis_ip, port=6379, db=1)
jdb = redis.Redis(host=redis_ip, port=6379, db=2, decode_responses=True)
img_db = redis.Redis(host=redis_ip, port=6379, db=3)


def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())


def _generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)


def _instantiate_job(jid, status, type, elevation, year, lat_start , long_start, lat_end , long_end):
    """
    Create the job object description as a python dictionary. Requires the job id, status,
    start and end parameters. types: line_graph, heatmap
    """
    return {'id': jid,
            'status': status,
            'type': type,
            'PARAMETER': elevation,
            'YEAR': year,
            'LAT': lat_start,
            'LON': long_start,
            'lat_end': lat_end,
            'long_end': long_end
            }


def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    jdb.hset(job_key, mapping=job_dict)
    return


def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)
    return


def add_job(
    status="submitted", type="line_graph", elevation = "WS10M", year = 2010, lat_start = 27.25, 
    long_start=-103.25, lat_end = 36.75, long_end=-93.75
    ):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, type, elevation, year, lat_start , long_start, lat_end , long_end)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict


def get_job_by_id(jid):
    """Return job dictionary given jid"""
    return (jdb.hgetall(_generate_job_key(jid).encode('utf-8')))


def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        _save_job(_generate_job_key(jid), job)

    else:
        raise Exception()
