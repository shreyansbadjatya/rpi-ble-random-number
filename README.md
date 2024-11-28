# rpi-ble-random-number
Small proof of concept to run BLE advertisement on bluetooth classic on rapberry pi 5 (Ubuntu 24.04). 
It run a Gatt server to communicate with BLE central.

This source code generates a random number and notify to the BLE central.

bluez_component is taken from  [https://github.com/fxwalsh/Bluetooth-Low-Energy-LED-Matrix.git](https://github.com/fxwalsh/Bluetooth-Low-Energy-LED-Matrix.git)

Steps: 
> `cd to rpi-ble-random-number`

> `python3 random_number_gatt_server.py`

Then run the following command in another terminal:

> `bluetoothctl`

> `power on`

> `agent on`

> `default-agent`

> `discoverable on`

> `advertising on`

This source provides one one service 0xFFF0 and that has once characteristic random number 0xFFF1.
Random number characteristic provides read and notify options.
