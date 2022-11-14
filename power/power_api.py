# https://github.com/jonghwanhyeon/python-switchbot
# pip3 install python-switchbot
# October 14, 2022

import logging
import uuid
from datetime import datetime, timezone

# add local directory to path
# https://fortierq.github.io/python-import/
# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[1]
# sys.path.insert(0,str(path_root))
# print(str(sys.path))
# sys.path.append(str(path_root))

#from power import switchbot
from .switchbot_api import SwitchBot
from dotmap import DotMap

# load token and secret from external file
# https://stackoverflow.com/a/67948155
# To get the token and secret, please refer to https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started
# copy switchbot_config/.token_example to switchbot_config/.token
# put your token and secret codes between the single quotes
# ensure .token is in your .gitignore so it is not checked into version control
exec(open('power/switchbot_config/.token').read())

def init_switchbot():
    switchbot = SwitchBot(token=your_switch_bot_token, secret=your_switch_bot_secret, nonce=str(uuid.uuid4()))
    # To list all devices
    #devices = switchbot.devices()
    # for device in devices:
    #     print(device.name, device.type, device.id, end='')
    #     plug = switchbot.device(device.id)
    #     print(plug.status())  
    return switchbot

def get_raw(device, keys):
    raw = DotMap()
    raw.name = device.name
    raw.type = device.type
    raw.id = device.id
    raw.status = keys
    return raw

def get_status(device, keys):
    
    utc_timestamp = datetime.utcnow().timestamp()
    utc_time = datetime.utcnow()
    local_timestamp = datetime.now().timestamp()
    local_time = datetime.now()
    
    status = DotMap()
    status.utc_time = utc_time
    status.local_time = local_time
    status.utc_timestamp = utc_timestamp
    status.local_timestamp = local_timestamp
    
    status.name = device.name
    status.type = device.type
    status.id = device.id
    # print(device.name, device.type, device.id, end='')
    # convert watts to kilowatts
    # convert minutes to hours
    # kwh = kw * hours
    status.kwh = f'{(keys["weight"] / 1000) * (keys["electricity_of_day"] / 60):.2f}'
    status.voltage_realtime = f'{keys["voltage"]:.2f}'
    status.watts_today = f'{keys["weight"]:.2f}'
    status.power = keys["power"]
    status.minutes_today = keys["electricity_of_day"]
    status.amps_realtime = f'{(keys["electric_current"] / 10):.2f}' # /10 to fix bug in api
    
    hours = f'{(keys["electricity_of_day"] // 60) :.0f}'  
    minutes = f'{(keys["electricity_of_day"] % 60) :.0f}' 
    status.on_hours_mins = f'{hours}:{minutes}'

    logging.info(status)
    return status


def power():
    switchbot = init_switchbot()
    # To list all devices
    results = []
    devices = switchbot.devices() # list of devices from the api
    for device in devices:
        # type == plug
        plug = switchbot.device(device.id) # new plug object for the device.id  
        keys = plug.status() # get plug status from the api 
        status = get_status(device,keys)
        status.z_raw = get_raw(device,keys)  
        results.append(status)
    return results


# If you already know a device id:
# device = switchbot.device(id='6055F92F6E2E')
# print(device.status())

#device.command('turn_off')

# To query a status of a device
# print(device.status())
# {'power': 'off'}

# To command actions,
# device.command('turn_on')
# device.command('turn_off')
# device.command('press')
# device.command('set_position', parameter='0,ff,80')

# # For some device types like Bot:
# bot = devices[0]
# bot.turn('on')
# bot.turn('off')
# bot.toggle()
# bot.press()

# # For some device types like Lock:
# lock = devices[1]
# lock.lock()
# lock.unlock()
# lock.toggle()