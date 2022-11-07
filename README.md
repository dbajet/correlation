
## Running the application with Docker

This is the preferred way as this limits the portability issues.

Copy the code from GitHub 
```
mkdir application
cd application
git clone git@github.com:dbajet/correlation.git
```

Create the Docker image
```
docker build -t correlation .
```

Create a container and run it
```
docker run -it -p 8080:8080 --rm --name correlation correlation:latest
```

When running the server, the application should be available: 
* HTML: [http://0.0.0.0:8080/?date=2022-11-01&format=html](http://0.0.0.0:8080/?date=2022-11-01&format=html)
* CSV: [http://0.0.0.0:8080/?date=2022-11-01](http://0.0.0.0:8080/?date=2022-11-01&format=html)

## Running the application locally

Python 3.8 needs to be installed.

Install the required libraries
```
sudo apt install python3-pip -y 
sudo apt install python3.8-venv -y 
```

Copy the code from GitHub 
```
mkdir application
cd application
git clone git@github.com:dbajet/correlation.git
```

Create the environment
```
python3.8 -m venv --copies ./env_correlation
source ./env_correlation/bin/activate
pip install -r correlation/requirements.txt
```


Run the server:
```
source ./env_correlation/bin/activate
cd correlation
./server.py
```

Run the tests:
```
source ./env_correlation/bin/activate
cd correlation
./tests.sh
```

Because of the limited 


The information allowing us to compute the location of the ISS limits the computation to a few weeks.
