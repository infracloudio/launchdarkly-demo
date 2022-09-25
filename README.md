# LauncDarkly Demo

# How to run locally

```sh
# Install virtualenv
flask --app app.run --debug run

```
## Using Docker Container
```sh
# Build Image
docker build . -t ld-demo
# Run container
docker run -p 5000:5000 ld-demo
```

# Migration & Upgrade

```sh
# Generate Migration
flask --app.run db migrate -m "Message here"
# upgrade db
flask --app.run db upgrade
```