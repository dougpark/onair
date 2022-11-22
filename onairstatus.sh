#!/bin/bash
# check the status of onAir and display it on the macOS menu bar using One Thing
# Connects to an onair server and retrieves the current status
# Requires macOS One Thing installed on this client computer
# Recommend using a utility like Lingon X to schedule this to run as cron job
# Run every 30 seconds seems to work fine
# Links
# [One Thing](https://apps.apple.com/us/app/one-thing/id1604176982?mt=12)
# [Lingon X](https://www.peterborgapps.com/lingon/)

# retrieve the status from the onair server
# update with your server url and port number
onair=$(curl -s https://onair.64zbit.com/status) 

# send status to One Thing
open --background "one-thing:?text=${onair}"
