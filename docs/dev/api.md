# API Specification
This site contains information about the different API routes. 
The API package has to be installed on the system to use the appropriate routes.

## GET `/api/v1/device/`
Get general device information.

### Response
```json
{
    "mgmt_interfaces" : [
        {
            "ip": "192.168.1.1",
            "physical_name": "ens0"
        },
        {
            "ip": "10.10.10.10",
            "physical_name": "ens1"
        }
    ],
    "logical_interfaces": [
        {
            "interface_id": 1,
            "logical_name": "LAN A",
            "physical_name": "eth1",
        },
        {
            "interface_id": 2,
            "logical_name": "LAN B",
            "physical_name": "eth2",
        },
        {
            "interface_id": 3,
            "logical_name": "LAN C",
            "physical_name": "eth3",
        },
        {
            "interface_id": 4,
            "logical_name": "LAN D",
            "physical_name": "eth4",
        }
    ],
}
```

## DELETE `/api/v1/device/reset/`
Reset all connections on the device.

### Response
```json
[
    "Device successfully resetted",
    200
]
```

## GET `/api/v1/connections/`
Get all connection information.

### Response
```json
{
    "connections": [
        {
            "connection_name": "Connection1",
            "connection_id": 1,
            "first_logical_interface_id": 1,
            "second_logical_interface_id": 2,
            "incoming":{
                "delay": 0,
                "packet_loss": 5,
                "bandwidth": 100,
                "jitter": 5
            },
            "outgoing":{
                "delay": 10,
                "packet_loss": 0,
                "bandwidth": 0,
                "jitter": 5
            }
        },
        {
            "connection_name": "Connection2",
            "connection_id": 2,
            "first_logical_interface_id": 3,
            "second_logical_interface_id": 4,
            "incoming":{
                "delay": 10,
                "packet_loss": 0,
                "bandwidth": 0,
                "jitter": 0
            },
            "outgoing":{
                "delay": 0,
                "packet_loss": 0,
                "bandwidth": 0,
                "jitter": 0
            }
        }
    ]    
}
```

## POST `/api/v1/connections/`
Create a single connection.

### Request
```json
{
    "connection_name": "new_name",
    "first_logical_interface_id": 2,
    "second_logical_interface_id": 3,
}
```

### Response
```json
{
    "connection_name": "new_name",
    "connection_id": 2,
    "first_logical_interface_id": 2,
    "second_logical_interface_id": 3,
}
```

## GET `/api/v1/connections/<connection_id>/`
Get specific connection information.

### Response
```json
{
    "connection_name": "Connection2",
    "connection_id": 2,
    "first_logical_interface_id": 2,
    "second_logical_interface_id": 3,
    "incoming":{
        "delay": 10,
        "packet_loss": 0,
        "bandwidth": 0,
        "jitter": 0
    },
    "outgoing":{
        "delay": 0,
        "packet_loss": 0,
        "bandwidth": 0,
        "jitter": 0
    }
}
```

## PUT `/api/v1/connections/<connection_id>/`
Update specific connection information.

### Request
```json
{
    "connection_name": "new-name",
    "connection_id": 2,
    "first_logical_interface_id": 2,
    "second_logical_interface_id": 3,
    "incoming":{
        "delay": 10,
        "packet_loss": 0,
        "bandwidth": 0,
        "jitter": 0
    },
    "outgoing":{
        "delay": 0,
        "packet_loss": 0,
        "bandwidth": 0,
        "jitter": 0
    }
}
```

### Response
```json
{
    "connection_name": "new-name",
    "connection_id": 2,
    "first_logical_interface_id": 2,
    "second_logical_interface_id": 3,
    "incoming":{
        "delay": 10,
        "packet_loss": 0,
        "bandwidth": 0,
        "jitter": 0
    },
    "outgoing":{
        "delay": 0,
        "packet_loss": 0,
        "bandwidth": 0,
        "jitter": 0
    }
}
```

## DELETE `/api/v1/connections/<connection_id>/`
Deletes a specific connection.

### Response
```json
[
    "Connection deleted successfully",
    200
]
```