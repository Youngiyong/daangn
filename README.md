# daangn-vote-api

##Swagger
```bash
http://localhost:8000/docs
```

## Basic installation
```bash
python3.7, docker, docker-compose
```

## Run local docker-composer and share workspace with local filesystem
```bash
docker-compose up
```

------------------------
## ETC

## Build for deploy

```bash
docker build -t daangn/vote-api .
```

## Run local docker

```bash
docker run -p 8000:8000 --name daangn --env-file .env daangn/vote-api uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
```

## Run local runserver

configure local venv and install dependencies 
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
