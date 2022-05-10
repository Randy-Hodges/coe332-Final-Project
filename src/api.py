import json
import csv
import glob
import logging
from flask import Flask, request
from jobs import rd, q, add_job, get_job_by_id

app = Flask(__name__)


@app.route('/', methods=['GET'])
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

# NOTE: need to heavily edit this
@app.route('/data', methods=['POST', 'GET'])
def download_data(): 
    """
    Fill out
    """
    if request.method == 'POST':

        rd.flushdb()
        import glob
        path = "/POWER_Regional*.csv"
        filenames = glob.glob(path)
        for count, filename in enumerate(filenames):
            logging.debug(f"{filename} going" )
            make_json(filename, "weather_data.json")
                                    
            # NOTE: Could grep a date in the filename to make the keys more consistent
            with open("weather_data.json") as f:
                rd.set(count, json.dumps(f))

            return 'Data has been loaded to Redis from file\n'

    elif request.method == 'GET':

        list_of_data = []

        for item in rd.keys():
            list_of_data.append(json.loads(rd.get(item)))

        return (f'{json.dumps(list_of_data, indent=2)}\n')

    else:

        return 'Only supports POST and GET methods\n'



@app.route('/jobs', methods=['GET'])
def jobs_api():
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
  curl localhost:5041/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"

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
        csvReader = csv.DictReader(csvf)
        
        # Convert each row into a dictionary
        # and add it to data
        for row in csvReader:
            
            # Assuming a column named 'No' to
            # be the primary key
            key = row['LAT'] + ", " + row['LON']
            data[key] = row

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

