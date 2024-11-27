import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import random
import time

# Define UUIDs for the GATT service and characteristics
SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHARACTERISTIC_UUID_READ = "abcdabcd-abcd-abcd-abcd-abcdabcdabcd"
CHARACTERISTIC_UUID_NOTIFY = "efghabcd-abcd-abcd-abcd-abcdabcdabcd"

class BlueZComponents:
    def __init__(self):
        # Set up D-Bus system bus for interaction with BlueZ
        self.bus = dbus.SystemBus()
        self.bluez = self.bus.get("org.freedesktop.DBus", "/org/freedesktop/DBus")
        self.adapter = self.bus.get("org.bluez", "/org/bluez/hci0")  # Assuming hci0 is the Bluetooth adapter
        self.advertising_manager = self.bus.get("org.bluez", "/org/bluez/advertising_manager1")  # BlueZ advertising manager
        self.advertisement_id = None  # Initialize the advertisement ID as None

    def create_advertisement(self):
        """Create BLE advertisement and register it"""
        advertisement_properties = {
            "Type": "peripheral",  # Advertisement type: peripheral
            "LocalName": "MyBLEDevice",  # Device name
            "ServiceUUIDs": [SERVICE_UUID]  # The GATT service UUID to advertise
        }

        # Register the advertisement with BlueZ
        advertisement = self.advertising_manager.RegisterAdvertisement(advertisement_properties)
        self.advertisement_id = advertisement  # Store the advertisement ID returned from BlueZ
        print(f"Advertisement registered with ID: {self.advertisement_id}")

    def start_advertising(self):
        """Start advertising the GATT service"""
        if not self.advertisement_id:
            self.create_advertisement()  # Create advertisement if not registered
        print("Starting advertisement...")
        self.adapter.StartAdvertising()  # Start advertising the service on the adapter

    def stop_advertising(self):
        """Stop advertising"""
        if self.advertisement_id:
            print("Stopping advertisement...")
            self.adapter.StopAdvertising()  # Stop advertising the service

# Example usage
bluez_components = BlueZComponents()
bluez_components.start_advertising()

# Start the GLib main loop for managing D-Bus events
GLib.MainLoop().run()
