﻿# elmec-connect-inv-ver
Get PID, VID, SN and IOS Versions from Cisco Routers from JSON input and save it to JSON output.

## JSON input format:  
{  
  "Hostname"  : "HOSTNAME"  
  "IP"        : "IP ADDRESS"  
}  
  
## JSON output format:  
{  
  "Hostname"  : "HOSTNAME"  
  "IP"        : "IP ADDRESS"  
  "PID"       : "PID"  
  "VID"       : "VID"  
  "SN"        : "SERIAL NUMBER"  
  "Version"   : "IOS VERSION"  
}  

## Usage:  
python3 elmec-connect-inv-ver.py  

You will then be required to insert an username and passowrd for SSH login.
