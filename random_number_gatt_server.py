#!/usr/bin/env python3
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import random
import time
import threading
import array
from bluez_components import *

class RandomNumberService(Service):
    RANDOM_NUMBER_SVC_UUID = '12345678-1234-5678-1234-56789abcdef0'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.RANDOM_NUMBER_SVC_UUID, True)
        self.add_characteristic(RandomNumberCharacteristic(bus, 0, self))

class RandomNumberCharacteristic(Characteristic):
    RANDOM_NUMBER_CHRC_UUID = '12345678-1234-5678-1234-56789abcdef1'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index,
            self.RANDOM_NUMBER_CHRC_UUID,
            ['read', 'notify'],  # Supports 'read' and 'notify'
            service)
        self.value = [0]
        self.notifying = False
        self.add_descriptor(
            CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        """BLE client reads the current random number."""
        print(f"Random Number Read: {self.value}")
        return self.value

    def StartNotify(self):
        """Start notifying the BLE client with random numbers."""
        if self.notifying:
            return
        self.notifying = True
        self.notify_random_number()

    def StopNotify(self):
        """Stop notifying the BLE client."""
        self.notifying = False

    def notify_random_number(self):
        """Send a random number to the client at 1-second intervals."""
        if not self.notifying:
            return

        self.value = [random.randint(0, 255)]  # Generate a random number (0-255)
        print(f"Sending Random Number: {self.value}")
        self.PropertiesChanged(GATT_CHRC_IFACE, {'Value': self.value}, [])

        # Call again after 1 second
        threading.Timer(1.0, self.notify_random_number).start()

class CharacteristicUserDescriptionDescriptor(Descriptor):
    CUD_UUID = '2901'

    def __init__(self, bus, index, characteristic):
        Descriptor.__init__(
            self, bus, index,
            self.CUD_UUID,
            ['read'],
            characteristic)
        self.value = array.array('B', b'Random Number Generator').tolist()

    def ReadValue(self, options):
        return self.value

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
        bus.get_object(BLUEZ_SERVICE_NAME, adapter),
        GATT_MANAGER_IFACE)

    app = Application(bus)
    random_number_service = RandomNumberService(bus, 0)
    app.add_service(random_number_service)

    mainloop = GObject.MainLoop()

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)

    mainloop.run()

if __name__ == '__main__':
    main()
