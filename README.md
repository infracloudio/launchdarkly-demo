# LaunchDarkly Demo

## How to run locally

```sh
# Install Virtualenv
pip install virtualenv

# Create Environment
virtualenv venv

# Activate Environment

# 1. For Linux
source venv/source/activate
# 2. For Windows
source venv/Scripts/activate
```

## Set Environment values
- Copy .env.sample file into same directory with name .env 
- Update LaunchDarkly Keys in it.

```
LD_SDK_KEY=#
LD_FRONTEND_KEY=#

```

## Run Flask Application.

```sh

# Make sure nothing is running on port 5000
flask --app app.run --debug run

# Open browser and go to this url.
# http://localhost:5000

```
## Using Docker Container
```sh
# Build Image
docker build . -t ld-demo
# Run container
docker run -p 5000:5000 ld-demo -e LD_FRONTEND_KEY="" -e LD_SDK_KEY=""
```
```
Using DockerHub Image

# Get tag value from Github Releases.

docker run -p 5000:5000 ld-demo -e LD_FRONTEND_KEY="" -e LD_SDK_KEY="" sudhanshuinfracloud/launchdarkly-demo:latest
```

## Migration & Upgrade

```sh
# Generate Migration
flask --app app.run db migrate -m "Message here"
# upgrade db
flask --app app.run db upgrade
```

## To Make API requests
- Install Postman or Curl