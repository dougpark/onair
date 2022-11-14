# Dockerfile-flask
# # https://medium.com/bitcraft/docker-composing-a-python-3-flask-app-line-by-line-93b721105777

# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3
# Set an environment variable with the directory
# where we'll be running the app in the container
ENV APP /app
# Create the directory and instruct Docker to operate
# from there from now on, in the container
RUN mkdir $APP
WORKDIR $APP
# Expose the port flask will listen on, from the container
EXPOSE 5000
# Copy the requirements file in order to install
# Python dependencies, copies into the container
COPY requirements.txt .
# Install Python dependencies, in the container
RUN pip install -r requirements.txt
# We copy the rest of the codebase into the image
# update - for development no need to copy, now link host and container volumes in docker-compose.yml
#COPY . .
# Start the flask app
# update - now started in docker-compose.yml
#CMD [ "python",  "app.py" ]
