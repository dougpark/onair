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

## Live Demo
* Check out [64zbit.com:5000/admin]()
* There's only one session so others may interrupt you

## Technical Details
* Works great on a Raspberry Pi
* Works great on any platform that can run a Docker container
* Written in Python with the Flask Server and Socket.io

## Default view 
* Share this view with family and coworkers
* Ex. onair.local
* Displays the standby and session messages
* During a session the current time and session remaining time are displayed

## Admin panel
* This url allows you to start and stop the session through the web interface
* Ex. onair.local/admin
* A stop and start button are displayed on the screen

## Defaults
```
* Here are the default time and messages which can be overridden with the api
* duration                      :120 minutes
* message                       :On Air
* standby                       :Stand By
* You can change these defaults by editing /onair_app/app.py
```

## Duration
* The session screen shows the current time and the remaining time
* The remaining time is set from the duration tag
* All it does is count down, and then counts up once it reaches zero
* It is there just as a reminder to wind things up

## API
* To make it easy to integerate with other workflows there is a simple api

### Start the session
```
* Ex. onair.local:5000/start?duration=60&message=Busy&standby=Available
* onair.local:5000              :your server name and port
* /start                        :is the route to start the session
* ?duration=60                  :sets the session duration to 60 minutes
* &message=Busy                 :sets the messsage displayed during the session
* &standby=Available            :sets the message when the session ends
```

### Stop the session
```
* Ex. onair.local:5000/stop
* Your server name and port     :onair.local:5000
* /stop                         :is the route to stop the session
```

### Status the session
```
* Ex. onair.local:5000/status
* /status                       :is the route to get a text based status of the system
* Returns a string of the current status
* Easy to parse on MacOS and display in your menubar with a script and One Thing
```

### Status the session with json
```
* Ex. onair.local:5000/json
* /json                         : is the route to get the full json status of the system
* Returns a json object of the current status
* Must be parsed to determine the current status
* onAir == True, then in session, False then in stand by mode
* If False then other info is pretty useless
* If True than other info is acurate at the time of response
```

## Server Installaton
* Download onair
    * Browse to [github/onair](https://github.com/dougpark/onair)
    * Click the big green Code button
    * Click the download ZIP button
    * Expand and move the onair folder to your local computer
    * or
    * Download with git
    * [Clone a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
* Raspberry Pi
    * TBD
* Docker
    * [Install Docker](https://docs.docker.com/engine/install/)
    * Open a terminal window
    * cd to the onair folder
    * ```cd onair```
    * start docker
    * ```docker-compose up -d```
    * on first run it will download all required files
    * to stop the onair server type ```docker-compose down```

## Start the server in developer mode
* in a bash or zsh terminal
* cd onair
* ./start_server.sh 
* to stop press control-c

## Start the server in production mode with Docker
* in a bash or zsh terminal
* cd onair
* docker-compose up -d
* to stop docker-compose down

## Client Installation
* Any client that can run a browser
* Works great in a "browser as an app" like [Unite](https://www.bzgapps.com/unite)
* A small Raspberry Pi with a built in touchscreen monitor works great as a table top display
* Works great on iOS when you 'Add to Home Screen'

## macOS and One Thing
* One Thing allows you to display one thing in the macOS menu bar
* [One Thing](https://apps.apple.com/us/app/one-thing/id1604176982?mt=12)
* See the included onairstatus.sh for an example
* Displays current session message on your menu bar
* Does not push to your client
* But you can poll frequently in your script for current status
* Can use Lingon X to schedule cron jobs on macOS, for example every 30 seconds
* [Lingon X](https://www.peterborgapps.com/lingon/)

## macOS/iOS and shortcuts
* Create a series of shortcuts with your favorite messages and durations

## Browsers and bookmarks
* Create a series of bookmarks with your favorite messages and durations

## Use PiHole
* Setup your local DNS such as onair.local for easy discovery

## Possible Modifications and Upgrades
* Theme your own color schemes, not everyone likes red and green
* Improve client UI/UX
* Pull in data from other API's
    - Current Temperature
    - Current Air Quality
    - Current status of smart home devices
    - Forcast and other weather info
* Clock
* Calendar
* Multi-session mode with user authentication
* [Integrate with Jason's e-ink display](https://sixcolors.com/post/2022/09/a-smart-e-ink-calendar-comes-to-my-kitchen/)
* You get the idea