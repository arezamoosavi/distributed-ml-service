
# load data:
curl -X POST "http://localhost:8080/v1/load_data/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "dataset=@advertising.csv;type=text/csv"

# response:
#{
#  "info": "ok",
#  "data_id": "d3782949b64d4b4ab7fa9a1450030593"
#}

# get available classifiers:
curl -X GET "http://localhost:8080/v1/model_types/" -H  "accept: application/json"

#response:
#{
#  "available_model_types": [
#    "logistic_regression",
#    "random_forest"
#  ]
#}

# train model:
curl -X POST "http://localhost:8080/v1/train_model/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"dataset_id\":\"2deaa795dda6413481e35308fc024d24\",\"model_type\":\"random_forest\",\"class_column\":\"Clicked on Ad\",\"feature_column\":\"Daily Time Spent on Site,Age,Area Income,Daily Internet Usage,Male\",\"test_ratio\":0.3}"

# response:
#{
#  "info": "ok",
#  "model_id": "3f13f74a43414a85b90f754ecbf6b997"
#}

# get model result:
curl -X POST "http://localhost:8080/v1/model_result/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"model_id\":\"22e8ad49167441508db1d25134f5b740\"}"

# response:
#{
#  "info": "ok",
#  "status": "ready",
#  "test_result": {
#    "model_type": "random_forest",
#    "class_column": "Clicked on Ad",
#    "feature_column": "Daily Time Spent on Site,Age,Area Income,Daily Internet Usage,Male",
#    "test_ratio": 0.3,
#    "result": {
#      "0": {
#        "precision": 0.948051948051948,
#        "recall": 0.9864864864864865,
#        "f1-score": 0.9668874172185431,
#        "support": 148
#      },
#      "1": {
#        "precision": 0.9863013698630136,
#        "recall": 0.9473684210526315,
#        "f1-score": 0.9664429530201343,
#        "support": 152
#      },
#      "accuracy": 0.9666666666666667,
#      "macro avg": {
#        "precision": 0.9671766589574808,
#        "recall": 0.966927453769559,
#        "f1-score": 0.9666651851193386,
#        "support": 300
#      },
#      "weighted avg": {
#        "precision": 0.9674316551028881,
#        "recall": 0.9666666666666667,
#        "f1-score": 0.9666622220246824,
#        "support": 300
#      }
#    },
#    "duration": 0.210334
#  }
#}

#download model:
curl -X POST "http://localhost:8080/v1/download_model/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"model_id\":\"22e8ad49167441508db1d25134f5b740\"}" -O -J

# response;
# it will download it to PWD