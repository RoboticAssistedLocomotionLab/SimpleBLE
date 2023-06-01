#!/usr/bin/env python3
import struct
import time
import keyboard
from getpass import getpass
from bluepy.btle import Peripheral, DefaultDelegate

YOUR_ADDRESS = "c0:98:e5:49:00:00" # Replace address with your device address
SERVICE_UUID = "c05899c4-457c-4c75-93ab-e55018bb3073"
CHAR_UUIDS = {"up": "c05899c5-457c-4c75-93ab-e55018bb3073",
        "down": "c05899c6-457c-4c75-93ab-e55018bb3073",
        "right": "c05899c7-457c-4c75-93ab-e55018bb3073",
        "left": "c05899c8-457c-4c75-93ab-e55018bb3073"}

#class CharDelegate(DefaultDelegate):
#    def __init__(self):
#        DefaultDelegate.__init__(self)
#
#    def handleNotification(self, cHandle, data):
#        print(cHandle)

class RobotController():

    def __init__(self, address):

        self.robot = Peripheral(YOUR_ADDRESS)
        #self.robot.setDelegate(CharDelegate())
        print("connected")

        self.pressed = {"up": False, "down": False, "right": False, "left": False}
        self.chars = {"up": None, "down": None, "right": None, "left": None}
        sv = self.robot.getServiceByUUID(SERVICE_UUID)
        # enumerate characteristic handles
        for char in CHAR_UUIDS:
            self.chars[char] = sv.getCharacteristics(CHAR_UUIDS[char])[0].getHandle()
        # enable notifications on chars
        for char in self.chars:
            self.robot.writeCharacteristic(self.chars[char]+1, b"\x01\x00")

        keyboard.hook(self.on_key_event)

    def on_key_event(self, event):
        # if a key unrelated to direction keys is pressed, ignore
        if event.name not in self.chars: return
        # if a key is pressed down
        if event.event_type == keyboard.KEY_DOWN:
            # if that key is already pressed down, ignore
            if self.pressed[event.name]: return
            # set state of key to pressed
            self.pressed[event.name] = True
            # write enable to direction characteristic
            self.robot.writeCharacteristic(self.chars[event.name], b'\x01')
        else:
            # set state of key to released
            self.pressed[event.name] = False
            # write disable to direction characteristic
            self.robot.writeCharacteristic(self.chars[event.name], b'\x00')

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.robot.disconnect()

with RobotController(YOUR_ADDRESS) as robot:
    getpass('Use arrow keys to control robot')
