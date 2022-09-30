# LaunchDarkly Demo

## How to run Flask Application


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

# Install all the requirements 
pip install -r requirements.txt

```

## Set Environment values
- Copy .env.sample file into same directory with name .env 
- Update LaunchDarkly Keys in it.
```
LD_SDK_KEY=#
LD_FRONTEND_KEY=#
```

## Run your Flask application

```sh
# Make sure nothing is running on port 5000
flask --app app.run --debug run
# Open browser and go to this url.
# http://localhost:5000

```
## Run Flask application using Docker.

You can run this application by creating a image and then running it or Using pre-built image available on docker hub.

### 1. Build and Run.

```sh
# Build Image
docker build . -t ld-demo
# Run container
docker run -p 5000:5000 ld-demo -e LD_FRONTEND_KEY="" -e LD_SDK_KEY=""
```
### 2. Using Pre-built Docker Image

```
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

## How to generate token for api requests


```
curl --location --request POST 'localhost:5000/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
     "email" : "USER_EMAIL_ID",
     "password" : "PASSWORD"
}'
```

## Available API endpoints

- `/api/login` - Generate Token for API calls.
- `/api/electronics` - Return List of Electronics Products.
- `/api/fashion` - Return List of Fashion Products.
- `/api/sale` - Return List of Products on sale.
## Implemented Flag keys and type

- `payment-gateway` type - boolean.
- `bell-icon` type - boolean.
- `ariticial-delay` type - boolean
- `max-like-allowed` type - number
- `add-to-like` type - boolean
- `redirect-to-sale` type - boolean
- `disable-registration` type - boolean
- `add-field-total` type - boolean
- `set-logging-level` type - number
- `sale-api` type - boolean
- `nav-dark` type - boolean
- `search-feature` type - boolean
- `dark-theme-button` type - boolean
