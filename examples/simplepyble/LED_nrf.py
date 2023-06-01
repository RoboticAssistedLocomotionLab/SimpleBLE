# Python Control Application for BLE
# Description:
#   The application is used for controlling a BLE compatible embedded system microcontroller. Plug in the UUID and identifier of your device and the application will connect with it. 
#
# Pre-requisite:
#   A bluetooth adapter compatible with BLE (Bluetooth Low Energy)
# Packages Needed:
#   simplepyble, keyboard, 

# Umer Huzaifa
# June 1, 2023


import simplepyble
import keyboard
import time

found_device = False

YOUR_ADDRESS = "c0:98:e5:49:aa:bb" # Replace address with your device address
YOUR_NAME = "LAB11"
SERVICE_UUID = "32e61089-2b22-4db5-a914-43ce41986c70"
CHAR_UUIDS = {"led":"32e68911-2b22-4db5-a914-43ce41986c70"}


LED_off = b'\x00'
LED_on = b'\x01'

##peripherals= []
##service_uuid = [] 
##characteristic_uuid = []
class RobotController():
    def __del__(self):
        print('Destructor called, Object deleted.')
    def print_conents(self):
        for characteristics in CHAR_UUIDS.get_keys():
            contents = self.peripheral.read(self.service_uuid, self.characteristic_uuid)
    def __init__(self, address):

        adapters = simplepyble.Adapter.get_adapters()
        
        found_device = False
        connect_device = False
        
        self.pressed = {"up": False, "down": False, "right": False, "left": False}
        self.chars = {"up": None, "down": None, "right": None, "left": None, "led": None}

        
        
        
        if len(adapters) == 0:
            print("No adapters found")

        # we can pick the top most in the list by default. If it does not work for you, print the list of adapters and choose the appropriate one.
        adapter = adapters[0]

        print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

        adapter.set_callback_on_scan_start(lambda: print("Scan started."))
        adapter.set_callback_on_scan_stop(lambda: print("Scan complete.\n"))
        adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))    
        
        # Scan for 3 seconds
        adapter.scan_for(3000)
        peripherals.append(adapter.scan_get_results())
        
        # Query the user to pick a peripheral
        print("Selecting the Peripheral from the Provided Address")
        for i, peripheral in enumerate(peripherals[0]):
            print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")            
            if peripheral.identifier()==YOUR_NAME:
                found_device = True
                connect_device = True
                self.peripheral=peripherals[0][i]
                print(f"Connecting to: {self.peripheral.identifier()} [{self.peripheral.address()}]")
                self.peripheral.connect()
                print("Successfully connected, listing services...")
                services = self.peripheral.services()
                service_characteristic_pair = []
                for service in services:
                    for characteristic in service.characteristics():
                        service_characteristic_pair.append((service.uuid(), characteristic.uuid()))
                        
                for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
                    print(f"{i}: {service_uuid} {characteristic}")
                
                    if service_uuid in SERVICE_UUID:#== "32e61089-2b22-4db5-a914-43ce41986c70":
                        self.service_uuid, self.characteristic_uuid = service_characteristic_pair[i]            
                        contents = self.peripheral.read(self.service_uuid, self.characteristic_uuid)
                        print(f"Contents: {contents}")
                        
                                   
                        while(True):
                            try:
                                time.sleep(0.3)
                                
                                print(f"Contents: {contents}")
                                if (connect_device==False):
                                    print("Safely exiting now")
                                    self.peripheral.disconnect()
                                    return
                                else:
                                    if keyboard.is_pressed("w"):
                                        self.peripheral.write_request(self.service_uuid, self.characteristic_uuid, LED_on)
                                    elif keyboard.is_pressed("s"):
                                        self.peripheral.write_request(self.service_uuid, self.characteristic_uuid, LED_off)
                            except KeyboardInterrupt:
                                print("Interrupted by Ctrl-C")
                                self.peripheral.disconnect()
                                print("Safely disconnecting now")
                                return
            

robot = RobotController(YOUR_ADDRESS)
del robot
