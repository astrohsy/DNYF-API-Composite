# DFNY Composite API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Deployment with ElasticBeanstalk

1. Activate Python virtual env
2. `pip install awsebcli`
3. **If your virtual env files are stored in the application folder, add them to `.ebignore` to prevent them from being uploaded to ElasticBeanstalk.**
4. *One-time*: `eb init` -> 1 -> DNYF-API-Composite -> N -> Python -> Python 3.8 -> N -> N
5. Create EB environment and deploy existing code: `eb create dnyf-composite-api-prod --single`
6. Deploy new code: `eb deploy dnyf-composite-api-prod`
7. Terminate EB environment: `eb terminate`

Terminating cleans up all resources associated with the environment.

## Development
### Install dependencies
```
pip install -r requirements-dev.txt
```

### Activate pre-commit hooks
```
pre-commit install
```

### Lint with Flake8
```
flake8 . --count --statistics
```

### DB Schema
The whole DB schema is re-created on app startup and data re-populated from the `sample_data.py` file

## Running the service
### Start up local API and DB
```bash
docker-compose -f docker-compose.yml up --build
```

### Only using DB with Docker
```bash
docker-compose -f docker-compose.yml up -d --build db
```

To start the API using a local Python environment:
```
uvicorn src.app:app --reload
```

### Debugging in VSCode
First build and start the containers in debug mode:
```bash
docker-compose -f docker-compose.debug.yml up --build
```

Then in VSCode:
- Navigate to *Run and Debug*
- Select the *Python: Remote Attach* configuration
- Start debugging

### Without Docker Compose (for reference)
```bash
docker volume create mysql
docker volume create mysql_config
docker network create dnyfnet
```

```bash
docker build --tag dnyf-composite-api .
```

```bash
docker run --name dnyf-composite-api \
    -p 8010:8010 \
    --network dnyfnet \
    -d dnyf-composite-api
```

```bash
docker run --rm --name dnyf-composite-db \
    --network dnyfnet \
    -v mysql:/var/lib/mysql \
    -v mysql_config:/etc/mysql \
    -e MYSQL_ROOT_PASSWORD=dbuser \
    -e MYSQL_USER=dbuser \
    -e MYSQL_PASSWORD=dbuser \
    -e MYSQL_DATABASE=dnyf-composite-db \
    -p 3306:3306 \
    -d mysql:8.0
```
