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
1. Start by editting the `Makefile` with your test editor of choice and replace `NSPACE` with your Docker Hub username, `RPORT` with your assigned Redis Port, and `FPORT` with your assigned Flask Port
2. Save and exit out and run the following command: `make cycle-all`
3. Once complete, you should now have running containers for the redis database, flask api, and worker. You can check that everything is running with: `docker ps -a`
4. If you want to push these images to Docker Hub, simply run `make push-all`

## Interacting with API:
## Creating Jobs:
## Retrieving Results from Jobs:
## Setting Up API on Kubernetes:
## Integration Testing:
