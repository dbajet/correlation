FROM python:3.8
RUN apt-get update -y

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install --upgrade setuptools wheel

# install the packages
WORKDIR /application/correlation/
COPY requirements.txt .
RUN python3.8 -m venv /application/env_correlation && \
    . /application/env_correlation/bin/activate && \
    pip install -r /application/correlation/requirements.txt

# create the menu
WORKDIR /application/
COPY menu.sh .
RUN chmod +x menu.sh

EXPOSE 8080

# add the code
WORKDIR /application/correlation/
COPY . /application/correlation/

CMD ["/application/menu.sh"]


# docker build -t correlation .
# docker run -it -p 8080:8080 --rm --name correlation correlation:latest
# docker exec -it correlation bash
