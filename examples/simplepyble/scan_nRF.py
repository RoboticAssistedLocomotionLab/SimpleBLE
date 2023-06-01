import simplepyble
import keyboard

found_device = False

YOUR_ADDRESS = "c0:98:e5:49:aa:bb" # Replace address with your device address
SERVICE_UUID = "32e61089-2b22-4db5-a914-43ce41986c70"
CHAR_UUIDS = {"up": "c05899c5-457c-4c75-93ab-e55018bb3073",
        "down": "c05899c6-457c-4c75-93ab-e55018bb3073",
        "right": "c05899c7-457c-4c75-93ab-e55018bb3073",
        "left": "c05899c8-457c-4c75-93ab-e55018bb3073",
        "led":"32e68911-2b22-4db5-a914-43ce41986c70"}


class RobotController():
    def __init__(self, address):

        adapters = simplepyble.Adapter.get_adapters()

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
        adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))
        # adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found a peripheral {peripheral.identifier()}"))

        # Scan for 5 seconds
        adapter.scan_for(5000)
        peripherals = adapter.scan_get_results()

        # Query the user to pick a peripheral
        print("Selecting the Peripheral from the Provided Address")
        for i, peripheral in enumerate(peripherals):
            print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")
            # if peripheral.address()=='c0:98:e5:49:00:00':
            # if peripheral.address()=='77:3c:03:42:93:4a':
                # print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")
            # if peripheral.identifier()=='Apple Pencil':
                # print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")
            if peripheral.identifier()=="LAB11":
                found_device = True
                peripheral=peripherals[i]
                print(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
                peripheral.connect()
                print("Successfully connected, listing services...")
                services = peripheral.services()
                service_characteristic_pair = []
                for service in services:
                    for characteristic in service.characteristics():
                        service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

                # Query the user to pick a service/characteristic pair
                # print("Please select a service/characteristic pair:")
                for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
                    print(f"{i}: {service_uuid} {characteristic}")
                
                    if service_uuid == "32e61089-2b22-4db5-a914-43ce41986c70":
                        service_uuid, characteristic_uuid = service_characteristic_pair[i]    
                # choice = int(input("Enter choice: "))
                        contents = peripheral.read(service_uuid, characteristic_uuid)
                        print(f"Contents: {contents}")
                        # Write the content to the characteristic
                        # Note: `write_request` required the payload to be presented as a bytes object.
                # Write the content to the characteristic
                        # content = int(input("Type in True or False to turn ON or OFF the LED. "))
                        content = b'\x00'
                        # if content == "True" or content == "False":
                        peripheral.write_request(service_uuid, characteristic_uuid, content) #str.encode(content))
                        # else:
                        content = b'\x01'
                        # if content == "True" or content == "False":
                        peripheral.write_request(service_uuid, characteristic_uuid, content) #str.encode(content))
                        peripheral.disconnect()    
                        break
                        
        if found_device!=True:         
            print("The device in interest was not found")  
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

if __name__ == "__main__":
              
    robot = RobotController(YOUR_ADDRESS)

    

   
