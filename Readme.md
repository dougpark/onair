# OnAir - a local area messaging system

* On Air allows you to notify those around you when you shouldn't be disturbed.

# Default view (share this view with family and coworkers)
* Ex. onair.local:5000
* Displays the standby and in session messages
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

# API
* To make it easy to integerate with other workflows there is a simple api

## Start the session
* Ex. onair.local:5000/start?duration=60&message=Busy&standby=Available
* Your server name and port     :onair.local:5000
* /start                        :is the api to start the session
* ?duration                     :sets the session duration to 60 minutes
* &message                      :sets the messsage displayed during the session
* &standby                      :sets the message when the session ends

## Stop the session
* Ex. onair.local:5000/stop
* Your server name and port     :onair.local:5000
* /stop                         :is the api to stop the session
