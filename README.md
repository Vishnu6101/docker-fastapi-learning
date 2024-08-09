# Django Learning FastAPI MongoDB

- This application is a simple todo app built using fastapi and mongodb
- The images of mongo db and mongo express are pulled from dockerhub
- A docker image for the fastapi app is built locally
- Docker compose is used to run all the containers

## Requirements
1. FastAPI
2. Uvicorn
3. motor
4. Docker
5. Anaconda / miniconda

## Steps
1. Create a Local Environment and activate it
```bash
conda create -n NAME python=3.10
conda activate NAME
```

2. Install the required packages
```bash
pip install fastapi uvicorn motor
```

3. Clone the repository
```bash
git clone https://github.com/Vishnu6101/docker-fastapi-learning.git
```

4. Build the docker image locally
```bash
docker build -t myapp:1.0 .
```

5. Run the docker-compose.yaml file
```bash
docker compose -f docker-compose.yaml up
```

To stop the containers
 ```bash
 docker compose -f docker-compose.yaml down
 ```