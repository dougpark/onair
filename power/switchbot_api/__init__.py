# https://github.com/jonghwanhyeon/python-switchbot
# pip3 install python-switchbot
# October 14, 2022


from typing import List
from .devices import Device
from .remotes import Remote

from .client import SwitchBotClient


class SwitchBot:
    def __init__(self, token: str, secret: str, nonce: str = ''):
        self.client = SwitchBotClient(token, secret, nonce)        

    def devices(self) -> List[Device]:
        response = self.client.get('devices')
        return [self.device(device['device_id'], **device)
                for device in response['body']['device_list']]
    
    def device(self, id: str, **extra) -> Device:
        return Device.create(client=self.client, id=id, **extra)

    def remotes(self) -> List[Remote]:
        response = self.client.get('devices')
        return [self.remote(remote['device_id'], **remote)
                for remote in response['body']['infrared_remote_list']]
    
    def remote(self, id: str, **extra) -> Remote:
        return Remote.create(client=self.client, id=id, **extra)
