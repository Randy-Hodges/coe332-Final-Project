import json
import csv
import glob
import logging
import os
from flask import Flask, request
from jobs import rd, q, add_job, get_job_by_id

app = Flask(__name__)


@app.route('/', methods=['GET'])
def disp_info() -> str:
    """
    Outputs string containing information on how to interact with this application. Details information on how to use each route and what each route does.
    
    Returns:
        output (string): String detailing all routes, their HTML method, and their outputs.    
    """
    return info()

@app.route('/<any>', methods=['GET'])
def help(any) -> str:
    """
    Outputs string containing information on how to interact with this application. Details information on how to use each route and what each route does.
    
    Returns:
        output (string): String detailing all routes, their HTML method, and their outputs.    
    """
    return info()


@app.route('/data', methods=['POST', 'GET'])
def download_data() -> str: 
    """
    This route contains 2 HTML methods:
    POST: Searches for any CSV data set starting with "POWER_Regional" and stores each data set as a JSON file. Loads the JSON file and 
          creates a new entry in the Redis database for each key:value pair. Returns string confirming completion of each step.
          
    GET:  Creates a list containing each key:value pair stored in the Redis database and outputs the list as a string.

    Returns:
        POST output (string): Short string confirming the successful loading of data from the file to Redis.
        
        GET  output (string): Large string containing all the data loaded into Redis.
    """
    if request.method == 'POST':

        rd.flushdb()
        path = "POWER_Regional*.csv"
        filenames = glob.glob(path)
        print(f"{len(filenames)} found" )
        if len(filenames) == 0:
            raise Exception("data set not found")
        for count, filename in enumerate(filenames):
            logging.debug(f"{filename} going" )
            make_json(filename, "weather_data.json")
                                    
            # NOTE: Could grep a date in the filename to make the keys more consistent
            with open("weather_data.json") as f:
                json_data = json.load(f)
                rd.set(str(count), json.dumps(json_data))

        return 'Data has been loaded to Redis from file\n'

    elif request.method == 'GET':

        list_of_data = []

        for item in rd.keys():
            list_of_data.append(json.loads(rd.get(item)))

        return (f'{json.dumps(list_of_data, indent=2)}\n')

    else:

        return 'Only supports POST and GET methods\n'


@app.route('/jobs', methods=['GET'])
def jobs_api() -> str:
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    if request.method == 'GET':
        return """
  To submit a job, do the following:
  curl localhost:5041/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"

"""


@app.route('/jobs/wind-speed', methods=['POST', 'GET'])
def jobs_wind_speed():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['start'], job['end']), indent=2) + '\n'

    elif request.method == 'GET':
        return """
  To submit a job, do the following:
  curl localhost:5011/jobs/wind-speed -X POST 

"""
    
    
@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid):
    """
    API route for checking on the status of a submitted job
    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
    
    # create a dictionary
    data = {}
    
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        count = 0
        while True:
            fr = csvf.readline() 
            print(fr)
            if fr == "-END HEADER-\n":
                break
            count += 1
            if count > 30:
                logging.error("'-END HEADER-' not found in data file")
                break
            
        csvReader = csv.DictReader(csvf)
        
        # Convert each row into a dictionary
        # and add it to data
        past_header = False
        count = 0
        for row in csvReader:
            
            # Assuming a column named 'No' to
            # be the primary key
            if len(row) == 0:
                continue
            
            key = row['LAT'] + ", " + row['LON'] #row[0] + ", " + row[1]# 
            data[key] = row
            # count += 1
            # if count < 10:
            #     print(f"********************* {row}")
            #     print(key)

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))


def info():
    """
    Informational
    """

    return """
  Try the following routes:

  /                GET    informational
  /data            GET    read data in database
  /data            POST   upload data to database
    
  /jobs            GET    info on how to submit job
  /jobs            POST   submit job
  /jobs/<jobid>    GET    info on job

"""


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

