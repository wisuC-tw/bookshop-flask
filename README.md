# Introduction

This is a bookshop app. 

## Stack
1. Python
2. Flask
3. MongoDB

# Getting Started

### Setup
Create a new virtual environment and activate it
```
$ python -m venv venv
$ source venv/bin/activate
```

Install the python packages in requirements.txt:
```
(venv) $ pip install -r requirements.txt
```

###  Local
In the root directory, run
```
python app.py
```
view the website at http://localhost:5000

### Running All Tests
```
python -m unittest -v
```

### Running Docker
In the tests folder, run
```
docker-compose up --build
```

### Running static code analysis
In the tests folder, run
```
sh scripts/run-bandit-check.sh
```

### Building wheel package
In the root directory, run
```
python setup.py bdist_wheel
```
the package will be in the dist/ folder

### Running spark jobs
In the root directory, run
```
spark-submit \
    --master local \
    --py-files dist/SomePackage-*.whl \
    jobs/spark_main.py
```
results in .json format will be written into `spark-outputs` folder
