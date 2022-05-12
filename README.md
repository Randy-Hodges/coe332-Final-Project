# Renewable Energy in Texas and Oklahoma: Wind Speeds

## Description:
With the concern of non-renewable energy source's sustainability and environmental impact on the rise, many consider switching to more renewable sources in the hopes of avoiding these issues in the future. One of the many methods used in this case include wind turbines, which rely on strong winds to generate energy mechanically. However, the question regarding whether the switch should be made remains, as it is totally dependent on the region and wind patterns in the area. This project aims to solve that problem. Utilizing NASA's POWER database, wind speed data from 2010 to 2020 at elevations of 10 m and 50 m in the Texas and Oklahoma region is collected. This project uses Python and Flask to create a REST API capable of creating, reading, updating, and deleting this data in a Redis database. The Flask app and Redis server are both deployable in Kubernetes as well. By utilizing jobs and worker, the API is also capable of analyzing specific data in the database and providing a visual representation of it in the form of a graph. Ultimately, this project analyzes given wind speed data in Texas and Oklahoma and better represents these values in specified locations. By doing so, users will have an idea of whether or not wind-powered energy is a good option in those areas.

## Getting Started:
To start, load all of the files in this repository to your machine. To do so:
1. Start a terminal and ssh into ISP02
2. In a new directory, input the following command: `git clone git@github.com:Randy-Hodges/coe332-Final-Project.git`
3. All files should be in that directory; check by inputting `ls`

## Setting Up API on ISP02:
With the files downloaded, we can now get started on setting up the images:
1. Start by editting the `Makefile` with your text editor of choice and replace `NSPACE` with your Docker Hub username, `RPORT` with your assigned Redis Port, and `FPORT` with your assigned Flask Port
2. Save and exit out and run the following command: `make cycle-all`
3. Once complete, you should now have running containers for the redis database, flask api, and worker. You can check if everything is running with: `docker ps -a`
4. If you want to push these images to Docker Hub, simply run `make push-all`

## Interacting with API:
To get a general overview of how to interact with the app, it is worth viewing the /help route which will give the following output:
```
  /                    GET    informational; prints this info
  /help                GET    informational; prints this info
  /data                GET    read data in database
  /data                POST   upload data to database
  /delete-data         GET    clears (deletes) all of the data in the redis database
        
  /jobs                GET    info on how to submit job
  /jobs/<jid>          GET    info on job
  /jobs/wind-speed     GET    submit a windspeed job
  /download/<jid>      GET    retrieve resulting chart from a job
```

After viewing this, the general workflow of using the app is as follows: 
- First ensure that the data is up-to-date by using the command “curl -X POST {api-route}/data”. This will either create the data in the database (if the database was empty) or update the data in the database. 
- Next one would submit a job through “curl {api-route}/jobs/wind-speed”. This creates a job and submits the job to the backend workers. Additional parameters can be added to the job (such as latitude, longitude and year) through adding query parameters to the end of the route. For example, “curl {api-route}/jobs/wind-speed?year=2011”. This route also returns an output with a job address. It is common to copy that job address (jid).
- Next one would view the status of that job though “curl {api-route}/jobs/<jid>”. This will tell if the job was submitted, is in progress, or has completed.
- Once completed, one would retrieve the chart created from the job through “curl {api-route}/download/<jid>”. It is common to redirect the output of this command to a file so that it can be accessed by the user. For example, “curl {api-route}/download/<jid> > my_new_file_name”.


## Description of Outputs:
Input: `/data`

Output:
```
    ...
    "36.75, -99.25, WS50M, 2020": {
      "PARAMETER": "WS50M",
      "YEAR": "2020",
      "LAT": "36.75",
      "LON": "-99.25",
      "JAN": "7.07",
      "FEB": "7.36",
      "MAR": "7.44",
      "APR": "7.62",
      "MAY": "7.08",
      "JUN": "8.88",
      "JUL": "6.05",
      "AUG": "6.5",
      "SEP": "6.5",
      "OCT": "7.63",
      "NOV": "7.87",
      "DEC": "6.96",
      "ANN": "7.24"
    },
    "36.75, -99.75, WS50M, 2020": {
      "PARAMETER": "WS50M",
      "YEAR": "2020",
      "LAT": "36.75",
      "LON": "-99.75",
      "JAN": "7.11",
      "FEB": "7.47",
      "MAR": "7.65",
      "APR": "7.77",
      "MAY": "7.23",
      "JUN": "9.08",
      "JUL": "6.18",
      "AUG": "6.57",
      "SEP": "6.65",
      "OCT": "7.6",
      "NOV": "7.97",
      "DEC": "7.11",
      "ANN": "7.36"
    }
  }
]
```
A large string listing all entries in the database as a dictionary of dictionaries. 
For each entry, there is a key containing the latitude, longitude, parameter, and year to represent each unique entry. Each of these keys are paired with a corresponding value pair that contains a dictionary with key:value pairs for the parameter, year, latitude, longitude, wind speeds for all 12 months, and average wind speed in the year.

## Creating Jobs:
To submit a job and begin retrieving more organized representations of specific data, we can utilize the route: `curl localhost:<FPORT>/jobs/wind-speed`. This should result in the following return message:
```
{"id": "3ed3c11d-0a4b-4d03-a1c9-2f412a74d6a2", "status": "submitted", "type": "line_graph", "PARAMETER": "WS10M", "YEAR": 2010, "LAT": 27.25, "LON": -100.25, "lat_end": 36.75, "long_end": -93.75}
```

By copying the given `id`, we can check the progress of the job by entering the `id` in place of `<jobid>` in the route: `curl localhost:<FPORT>/jobs/<jobid>`. This should result in an output similar to this:
```
{
  "id": "3ed3c11d-0a4b-4d03-a1c9-2f412a74d6a2",
  "status": "in progress",
  "type": "line_graph",
  "PARAMETER": "WS10M",
  "YEAR": "2010",
  "LAT": "27.25",
  "LON": "-100.25",
  "lat_end": "36.75",
  "long_end": "-93.75"
}
```

Once the `status` updates to `finished`, we can now start downloading and retrieving the results from our job.
## Retrieving Results from Jobs:
To retrieve our results, we simply utilize the command `curl localhost:<FPORT>/download/<jobid> > <filename>.png`, replacing `<filename>` with a name of your choice. This saves the graph generated by the worker as a png file titled `<filename>`.png. We can then move and view this graph onto our local machine with scp by following the steps below:
1. Open a new terminal on your local machine and enter `cd ./Desktop/` to move to your desktop
2. Scp the image to your desktop with: `scp <username>@isp02.tacc.utexas.edu:<pwd>/<filename>.png .` 
    - NOTE: replace `<pwd>` with the pathway directory on ISP02 containing `<filename>`.png; can be found by entering the command `pwd` on ISP02 terminal
3. The image is now on your desktop and you can view it there.

    
## Setting Up API on Kubernetes:
To set up and perform all of these processes in Kubernetes:
1. Ssh into Kubernetes with: `ssh <username>@coe332-k8s.tacc.cloud`
2. Make a new directory and clone this repository again with: `git clone git@github.com:Randy-Hodges/coe332-Final-Project.git`
3. Deploy all services/deployments with the command: `kubectl apply -f kubernetes/prod/`
4. Check that all pods, deployments, and services are deployed with:
    ```
    kubectl get pods
    kubectl get deployments
    kubectl get services
    ```
5. When all of the deployments are ready with status as running, we can utilize the API in the same way we utilized them in ISP02
## Integration Testing:
Testing can be done through running the command pytest in the repository.
## Citations:
“The POWER Project.” *NASA Prediction Of Worldwide Energy Resources*, NASA, https://power.larc.nasa.gov/. 
