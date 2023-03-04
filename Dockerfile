# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-buster

# Copy local code to the container image.
ENV PORT 8080
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . /app

# Install production dependencies.
RUN apt-get update && apt-get install -y
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process_quote and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app