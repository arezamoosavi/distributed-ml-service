# distributed-ml-service
In this project based on user's dataset and required model type the a classifier will be trained!

## Run

for running the project:
###first
```bash
docker-compose up -d mysql minio rabbitmq
```
After stable running:
###second
```bash
docker-compose up -d celery flower apis
```
##stop and remove
```bash
docker-compose down -v
```

## Usage
api docs:
```bash
http://localhost:8080/docs
```
flower monitoring:
```bash
http://localhost:8888
```
minio file storage:
```bash
http://localhost:9000
```
rabbitmq:
```bash
http://localhost:15672
```
mysql
```bash
http://localhost:3306
```
## More Documnt
####[ml-pipe.herokuapp.com](https://ml-pipe.herokuapp.com/docs#/)
### [Medium](https://medium.com/@sdamoosavi/ml-microservice-with-nameko-to-implement-a-predictive-maintenance-application-f59d4ed60be3)

