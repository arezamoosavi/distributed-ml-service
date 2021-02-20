# distributed-ml-service
In this project based on user's dataset and required model type the a classifier will be trained!

## Run

for running the project:
### first
```bash
docker-compose up -d mysql minio rabbitmq
```
After stable running:
### second
```bash
docker-compose up -d celery flower apis
```
## stop and remove
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
## Example
In the example directory there is advertising.csv file as dataset:
### Loading data
The api returns this:
```json
{
  "info": "ok",
  "data_id": "cfe3ee4dcf8448038cbe386b54a4cae2"
}
```
### Train Classifier
The data for posting would be like this:
 ```json
{
  "dataset_id": "cfe3ee4dcf8448038cbe386b54a4cae2",
  "model_type": "random_forest",
  "class_column": "Clicked on Ad",
  "feature_column": "Daily Time Spent on Site,Age,Area Income,Daily Internet Usage,Male",
  "test_ratio": 0.3
}
```
Then the api returns:
```json
{
  "info": "ok",
  "model_id": "0bb58a0465c544eb8ccc4d0300a0ec79"
}
```
### Model results and Download
Only model_id is enough:
```json
{
  "model_id": "0bb58a0465c544eb8ccc4d0300a0ec79"
}
```
## More
A simple version of the app is deployed on heroku and it is here:
#### [ml-pipe.herokuapp.com](https://ml-pipe.herokuapp.com/docs#/)
### [Medium](https://sdamoosavi.medium.com/asynchronouse-distributed-ml-platform-751e3beee333)

