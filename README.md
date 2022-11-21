# DFNY Composite API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

## Running the service
### Start up local API
```bash
docker-compose -f docker-compose.yml up --build
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
docker build --tag dnyf-composite-api .
```

```bash
docker run --name dnyf-composite-api \
    -p 8010:8010 \
    --network dnyfnet \
    -d dnyf-composite-api
```
