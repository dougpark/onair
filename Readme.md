# OnAir - a local area messaging system
* On Air allows you to notify those around you when you shouldn't be disturbed
* Version 1.0, be nice I'm a hobbyist

## Use Case
* For example:
* When you are recording a podcast
* When recording a youTube video
* When in a meeting at the office
* When on a Zoom meeting
* When you are studying
* When you are taking a nap
* When you just *##^$ just want to be left alone

## Technical Details
* Works great on a Raspberry Pi
* Works great on any platform that can run a Docker container
* Written in Python with the Flask Server and Socket.io

# Default view 
* Share this view with family and coworkers
* Ex. onair.local:5000
* Displays the standby and session messages
* During a session the current time and session remaining time are displayed

# Admin panel
* This url allows you to start and stop the session through the web interface
* Ex. onair.local:5000/admin
* A stop and start button are displayed on the screen

# Defaults
* Here are the default time and messages which can be overridden with the api
* duration                      :120 minutes
* message                       :On Air
* standby                       :Stand By
* You can change these defaults by editing /onair_app/app.py

# Duration
* The session screen shows the current time and the remaining time
* The remaining time is set from the duration tag
* All it does is count down, and then counts up once it reaches zero
* It is there just as a reminder to wind things up

# API
* To make it easy to integerate with other workflows there is a simple api

## Start the session
* Ex. onair.local:5000/start?duration=60&message=Busy&standby=Available
* Your server name and port     :onair.local:5000
* /start                        :is the route to start the session
* ?duration=60                  :sets the session duration to 60 minutes
* &message=Busy                 :sets the messsage displayed during the session
* &standby=Available            :sets the message when the session ends

## Stop the session
* Ex. onair.local:5000/stop
* Your server name and port     :onair.local:5000
* /stop                         :is the route to stop the session

## Status the session
* Ex. onair.local:5000/status
* Returns a string of the current status
* Easy to parse on MacOS and display in your menubar with a script and One Thing

# Server Installaton
* Raspberry Pi
* Docker

# Start the server in developer mode
* in a bash or zsh terminal
* cd onair
* ./start_server.sh 
* to stop press control-c

# Start the server in production mode with Docker
* in a bash or zsh terminal
* cd onair
* docker-compose up -d
* to stop docker-compose down

# Client Installation
* Any client that can run a browser
* A small Raspberry Pi with a built in touchscreen monitor works great as a table top display
* Works great on iOS when you 'Add to Home Screen'

# macOS and One Thing
* Displays current session message on your menu bar
* Does not push to your client
* But you can poll frequently in your script for current status

# macOS/iOS and shortcuts
* Create a shortcut with your favorite messages and durations

# Browsers and bookmarks
* Create a bookmark with your favorite messages and durations

# Possible Modifications and Upgrades
* Pull in data from other API's
-- Current Temperature
-- Current Air Quality
-- Current status of smart home devices
-- Forcast and other weather info
-- You get the idea