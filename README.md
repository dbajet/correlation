## Notes

The `correlation` application explores the correlation between the Apple stock and the International Space Station (ISS) position.

This correlation is computed using the last 5 closing values of the `APPL` symbol preceding a provided date and
the distance in kilometers of the ISS to Wall Street at that time.

A test web server serves the result either as a CSV or an HTML page.

In addition of the correlation matrix, the result contains the data retrieved.

_While the logic is mostly tested, the coverage provided when running the tests is just indicative that no runtime errors would occur._

## Running the application with Docker

This is the preferred way as this limits the portability issues.

Copy the code from GitHub

```
mkdir application
cd application
git clone git@github.com:dbajet/correlation.git
cd correlation
```

Create the Docker image

```
docker build -t correlation .
```

Create a container and run it

```
docker run -it -p 8080:8080 --rm --name correlation correlation:latest
```

When running the web server, the application should be available:

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
./run_server.py
```

Run the tests (pytest):

```
source ./env_correlation/bin/activate
cd correlation
./run_tests.sh
```

Run the static checks (mypy):

```
source ./env_correlation/bin/activate
cd correlation
./run_mypy.sh
```

