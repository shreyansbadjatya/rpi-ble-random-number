import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import random
import time

# BlueZ service paths and D-Bus objects
BLUEZ_SERVICE = "org.freedesktop.DBus"
GATT_SERVICE_PATH = "/org/bluez/gatt_server1"
ADVERTISING_MANAGER_PATH = "/org/bluez/advertising_manager1"
ADAPTER_PATH = "/org/bluez/hci0"  # Bluetooth adapter (hci0)

# UUIDs for the GATT service and characteristics
SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHARACTERISTIC_UUID_READ = "abcdabcd-abcd-abcd-abcd-abcdabcdabcd"
CHARACTERISTIC_UUID_NOTIFY = "efghabcd-abcd-abcd-abcd-abcdabcdabcd"

# Characteristic value that will be read or notified
CHARACTERISTIC_VALUE = "Initial Value"

# Advertisement properties
ADVERTISER_PROPERTIES = {
    "Type": "peripheral",  # Peripheral advertisement
    "LocalName": "MyGATTServer",
    "ServiceUUIDs": [SERVICE_UUID],
    "Appearance": 1280,
    "ManufacturerData": b'\x01\x02\x03\x04',  # Optional custom manufacturer data
}

# Store the advertisement ID
advertisement_id = None

# Setup DBus main loop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

# Obtain the BlueZ object from the D-Bus system bus
bluez = bus.get("org.freedesktop.DBus", "/org/freedesktop/DBus")
adapter = bus.get("org.freedesktop.DBus.ObjectManager", ADAPTER_PATH)
advertising_manager = bus.get("org.freedesktop.DBus.ObjectManager", ADVERTISING_MANAGER_PATH)


# Define a GATT server class that implements read and notify characteristics
class GattServer:

    def __init__(self):
        self.characteristic_value = CHARACTERISTIC_VALUE
        self.advertisement_id = None

    def read_characteristic(self, characteristic_path):
        """Read the value of the characteristic"""
        print(f"Reading characteristic {characteristic_path}")
        return dbus.ByteArray(self.characteristic_value.encode())

    def notify_characteristic(self, characteristic_path):
        """Notify characteristic change to clients"""
        new_value = "Updated Value " + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
        self.characteristic_value = new_value
        print(f"Notifying clients with new value: {new_value}")
        return dbus.ByteArray(new_value.encode())

    def register_characteristics(self):
        """Register characteristics for read and notify operations"""
        gatt_service = bus.get("org.freedesktop.DBus.ObjectManager", GATT_SERVICE_PATH)

        # Register Read characteristic
        gatt_service.RegisterCharacteristic(
            CHARACTERISTIC_UUID_READ,
            dbus.Interface(gatt_service, "org.freedesktop.DBus.Properties").Get(
                "org.freedesktop.DBus.Properties", "Read"
            ),
            dbus_interface="org.freedesktop.DBus"
        )

        # Register Notify characteristic
        gatt_service.RegisterCharacteristic(
            CHARACTERISTIC_UUID_NOTIFY,
            dbus.Interface(gatt_service, "org.freedesktop.DBus.Properties").Get(
                "org.freedesktop.DBus.Properties", "Notify"
            ),
            dbus_interface="org.freedesktop.DBus"
        )


    def create_advertisement(self):
        """Create BLE advertisement"""
        global advertisement_id
        advertisement = advertising_manager.RegisterAdvertisement(ADVERTISER_PROPERTIES)
        advertisement_id = advertisement
        print(f"Advertisement registered with ID: {advertisement_id}")

    def start_advertising(self):
        """Start the BLE advertisement"""
        if not advertisement_id:
            self.create_advertisement()
        print("Starting BLE advertising...")
        adapter.StartAdvertising()

    def stop_advertising(self):
        """Stop the BLE advertisement"""
        if advertisement_id:
            print("Stopping BLE advertising...")
            adapter.StopAdvertising()

# Create the GattServer object
gatt_server = GattServer()

def main_loop():
    """Main loop for GATT server to keep running"""
    gatt_server.start_advertising()

    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        gatt_server.stop_advertising()
        print("Advertising stopped.")


if __name__ == "__main__":
    main_loop()
