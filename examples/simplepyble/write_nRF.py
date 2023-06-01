import simplepyble
import keyboard
from functools import partial
found_device = False

YOUR_ADDRESS = "c0:98:e5:49:aa:bb" # Replace address with your device address
SERVICE_UUID = "32e61089-2b22-4db5-a914-43ce41986c70"
CHAR_UUIDS = {"up": "c05899c5-457c-4c75-93ab-e55018bb3073",
        "down": "c05899c6-457c-4c75-93ab-e55018bb3073",
        "right": "c05899c7-457c-4c75-93ab-e55018bb3073",
        "left": "c05899c8-457c-4c75-93ab-e55018bb3073",
        "led":"32e68911-2b22-4db5-a914-43ce41986c70"}
LED_off = b'\x00'
 
LED_on = b'\x01'

peripherals= []
service_uuid = [] 
characteristic_uuid = []
class RobotController():
    def __del__(self):
        print('Destructor called, Employee deleted.')
    def __init__(self, address):

        adapters = simplepyble.Adapter.get_adapters()
        
        found_device = False
        connect_device = False
        
        self.pressed = {"up": False, "down": False, "right": False, "left": False}
        self.chars = {"up": None, "down": None, "right": None, "left": None, "led": None}

        
        
        
        if len(adapters) == 0:
            print("No adapters found")

        # Query the user to pick an adapter
        # print("Please select an adapter:")
        # for i, adapter in enumerate(adapters):
        #     print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

        # choice = int(input("Enter choice: "))
        # adapter = adapters[choice]
        adapter = adapters[0]

        print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

        adapter.set_callback_on_scan_start(lambda: print("Scan started."))
        adapter.set_callback_on_scan_stop(lambda: print("Scan complete.\n"))
        # adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))
        # adapter.set_callback_on_scan_found(lambda peripheral: peripherals.append(peripheral)))
        adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found a peripheral {peripheral.identifier()}"))
        
        # Scan for 5 seconds
        adapter.scan_for(5000)
        peripherals.append(adapter.scan_get_results())
        
        # Query the user to pick a peripheral
        print("Selecting the Peripheral from the Provided Address")
        for i, peripheral in enumerate(peripherals[0]):
            print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")            
            if peripheral.identifier()=="LAB11":
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
                        
                        keyboard.hook(self.on_key_event)#, peripheral)
                        # key = partial(self.on_key_event)                        
                        while(True): 
                            if (connect_device==False):
                                print("Safely exiting now")
                                return
                            else:
                                pass                                           
                    

            # if (found_device==False):
            #     print("The device in interest was not found")              
            #     return 
            
                    
    def clear_pressed(self):
        for i in self.pressed.keys():
            self.pressed[i]=False
    
    def set_pressed(self):
        for i in self.pressed.keys():
            self.pressed[i]=True
            
    def on_key_event(self, event): #, peripheral):
       
                
        if event.name not in ["DOWN", "UP"]:
            print(f"Irrelevant key {event.name} pressed.")
            return 
        if self.pressed[event.name]: 
            print(f"already pressed {event.name}")
            return
        if event.event_type == keyboard.KEY_DOWN:
            print("DOWN key pressed")
            # if that key is already pressed down, ignore
            
            # set state of key to pressed
            self.pressed[event.name] = True
            # write enable to direction characteristic
            self.peripheral.write_request(self.service_uuid, self.characteristic_uuid, LED_off) #str.encode(content))
            self.clear_pressed()
            return
            # return 'DOWN'
        elif event.event_type == keyboard.KEY_UP:
            print("UP key pressed")
            
            # set state of key to prd                                          essed
            # self.pressed[event.name] = True
            # write enable to direction characteristic
            self.peripheral.write_request(service_uuid, characteristic_uuid, LED_on) #str.encode(content))
            # return 'DOWN'
            # if content == "True" or content == "False":
            # peripheral.write_request(service_uuid, characteristic_uuid, content) #str.encode(content))
            self.clear_pressed()
            return
        else:
            # return 'QUIT'
            print(f"Irrelevant key {event.name} pressed")
            # self.pressed["UP"] = False
            connect_device = False
            self.peripheral.disconnect()    
            print("Disconnecting Now")
            return 
            # break
        # contents = self.peripheral.read(self.service_uuid, self.characteristic_uuid)
        # print(f"Contents: {contents}")
        # return

robot = RobotController(YOUR_ADDRESS)
del robot