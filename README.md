# rpi-ble-random-number
BLE random number gatt server on raspberry pi 

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

# Cisco IoT Orchestrator API: 

# 1. Onboard Device

This API call is used to register a new device in Cisco IoT Orchestrator using the SCIM protocol.

## Endpoint
**`POST`** `https://[server]:8081/scim/v2/Devices`

# Example cURL Command

```shell
curl -k --location "https://[SERVER]:8081/scim/v2/Devices" \
--header "x-api-key: [API-KEY]" \
--header "Content-Type: application/json" \
--data '{
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:Device",
        "urn:ietf:params:scim:schemas:extension:ble:2.0:Device",
        "urn:ietf:params:scim:schemas:extension:endpointapps:2.0:Device"
    ],
    "deviceDisplayName": "[Device-Name]",
    "adminState": true,
    "urn:ietf:params:scim:schemas:extension:ble:2.0:Device": {
        "versionSupport": [
            "5.0",
            "5.1",
            "5.2",
            "5.3",
            "5.4"
        ],
        "deviceMacAddress": "[Bluetooth-Device-MAC]",
        "isRandom": false,
        "mobility": false,
        "pairingMethods": [
            "urn:ietf:params:scim:schemas:extension:pairingNull:2.0:Device",
            "urn:ietf:params:scim:schemas:extension:pairingJustWorks:2.0:Device"
        ],
        "urn:ietf:params:scim:schemas:extension:pairingNull:2.0:Device": null,
        "urn:ietf:params:scim:schemas:extension:pairingJustWorks:2.0:Device": {
            "key": null
        }
    },
    "urn:ietf:params:scim:schemas:extension:endpointAppsExt:2.0:Device": {
        "onboardingUrl": "[OnboardApplication]",
        "deviceControlUrl": [
            "[ControlApplication]"
        ],
        "dataReceiverUrl": [
            "[DataApplication]"
        ]
    }
}'

```

> [!Important]
> 
> Replace [SERVER] with the actual IP or hostname of the IoT Orchestrator instance.
> 
> Replace [API_KEY] with OnboardApplication Key.
> 
> Replace [Device-Name] with any name of your choice, which is identifiable.
> 
> Replace [Bluetooth-Device-MAC] with the bluetooth device MAC ID.
>
> Sucessful response of this API will provide a BLE-Device-ID, which will be used an several API calls.

> [!CAUTION]
> Use correct name of the [OnboardApplication], [ControlApplication] and [DataApplication]


# 2. Connect Device

This API call is used to connect an onboarded device in Cisco IoT Orchestrator.

## Endpoint
**`POST`** `https://[server]:8081/control/connectivity/connect`


# Example cURL Command

```shell
curl -k --location 'https://[SERVER]/control/data/read' \
--header 'x-api-key: [API-KEY]' \
--header 'Content-Type: application/json' \
--data '
{
"technology": "ble",
"id": "[BLE-Device-ID]",
"ble": {
"serviceID": "fff0",
"characteristicID": "fff1"
},
"controlApp": "[ControlApplication]"
}'
```

> [!Important]
> 
> Replace [SERVER] with the actual IP or hostname of the IoT Orchestrator instance.
> 
> Replace [API_KEY] with OnboardApplication Key.
> 
> Replace [BLE-Device-ID] with the bluetooth device ID from onboarding API response.
>
> ServiceID and characteristicID are source code dependent, if any change is required, then update the source code and relevant API calls.

> [!CAUTION]
> Use correct name of the [ControlApplication]

# 3. Register Data Application

This API call is used to register a data application

## Endpoint
**`POST`** `https://[server]:8081/control/registration/registerDataApp`


# Example cURL Command

```shell
curl -k --location 'https://[SERVER]/control/registration/registerDataApp' \
--header 'Content-Type: application/json' \
--header 'x-api-key: [API-KEY]' \
--data '
{
"controlApp": "[ControlApplication]",
"topic": "[rpi/ble/randomnumber]",
"dataApps": [
{
"dataAppID": "[DataApplication]"
}
]
}'
```

> [!Important]
> 
> Replace [SERVER] with the actual IP or hostname of the IoT Orchestrator instance.
> 
> Replace [API_KEY] with OnboardApplication Key.
> 
> Replace [rpi/ble/randomnumber] with relevant topic, or just use it as is: rpi/ble/randomnumber.

> [!CAUTION]
> Use correct name of the [ControlApplication] and [DataApplication]


# 4. Register topic

This API call is used to register a topic

## Endpoint
**`POST`** `https://[server]:8081/control/registration/registerTopic`


# Example cURL Command

```shell
curl -k --location 'https://[SERVER]/control/registration/registerTopic' \
--header 'Content-Type: application/json' \
--header 'x-api-key: [API-KEY]' \
--data '
{
"technology": "ble",
"ids": [
"[BLE-Device-ID]"
],
"controlApp": "[ControlApplication]",
"topic": "[rpi/ble/randomnumber]",
"dataFormat": "default",
"ble": {
"type": "gatt",
"serviceID": "FFF0",
"characteristicID": "FFF1"
}
}'
```

> [!Important]
> 
> Replace [SERVER] with the actual IP or hostname of the IoT Orchestrator instance.
> 
> Replace [API_KEY] with OnboardApplication Key.
> 
> Replace [BLE-Device-ID] with the bluetooth device ID from onboarding API response.
> 
> Replace [rpi/ble/randomnumber] with same as in register data application API.
>
> ServiceID and characteristicID are source code dependent, if any change is required, then update the source code and relevant API calls. Keep them same as in connect API.

> [!CAUTION]
> Use correct name of the [ControlApplication]

# 5. Subscribe to Notification

This API call is used to subscribe to notification data from BLE

## Endpoint
**`POST`** `https://[server]:8081/control/data/subscribe`


# Example cURL Command

```shell
curl -k --location 'https://[SERVER]:8081/control/data/subscribe' \
--header 'Content-Type: application/json' \
--header 'x-api-key: [API-KEY]' \
--data '
{
"technology": "ble",
"id": "[BLE-Device-ID]",
"ble": {
"serviceID": "fff0",
"characteristicID": "fff1"
},
"controlApp": "[ControlApplication]"
}'
```
> [!Important]
> 
> Replace [SERVER] with the actual IP or hostname of the IoT Orchestrator instance.
> 
> Replace [API_KEY] with OnboardApplication Key.
> 
> Replace [BLE-Device-ID] with the bluetooth device ID from onboarding API response.
>
> ServiceID and characteristicID are source code dependent, if any change is required, then update the source code and relevant API calls. Keep them same as in connect API.

> [!CAUTION]
> Use correct name of the [ControlApplication]



# 6. Reading Data via MQTT
```shell
mosquitto_sub -h [SERVER] -p 41883 -t [rpi/ble/randomnumber] -u [DataApplication] --pw [API_KEY]
```

> [!Important]
> 
> Replace [SERVER] with the actual IP or hostname of the IoT Orchestrator instance.
> 
> Replace [API_KEY] with DataApplication Key.
> 
> Replace [rpi/ble/randomnumber] with same as in register data application API.

> [!CAUTION]
> Use correct name of the [DataApplication]


