import warnings
from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings():
    # Ignore blowfish deprecation warning currently affecting transport in paramiko library
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, BadHostKeyException, SSHException
from getpass import getpass
from re import match
import json
import regex

# Load source list
with open("in.json") as f:
    list = json.load(f)
# Output JSON array
hosts_out = []

# Get login informations
SSH_USERNAME = input("Username: ")
SSH_PASSWORD = getpass()

# Create SSH Client with AutoAddPolicy for unknown hosts
ssh_client = SSHClient()
ssh_client.set_missing_host_key_policy(AutoAddPolicy())

for host in list:
    inventory_all = []
    hostname = host["Hostname"]
    ip = host["IP"]
    print(f"Hostname: {hostname}")

    try:
        ssh_client.connect(ip, username=SSH_USERNAME, password=SSH_PASSWORD)    # Connect to host
        ssh_in, ssh_out, ssh_err = ssh_client.exec_command("show inventory")            # Execute inventory command
        for line in ssh_out.readlines():
            line = line.rstrip()
            if not match(regex.EMPTY_LINE, line):   # Remove all empty lines from command output
                if (match(regex.CISCO_INVENTORY_PID, line) and
                    match(regex.CISCO_INVENTORY_VID, line) and
                    match(regex.CISCO_INVENTORY_SN, line)):     # Match only usefull lines (will match device and power supply)
                    inventory_all.append(line)
        inventory_device = inventory_all[0].split(",")          # Take only device line and split it by comma
        # Clean outputs
        pid = inventory_device[0].replace("PID: ","").replace(" ", "").rstrip()
        vid = inventory_device[1].replace("VID: ","").replace(" ", "").rstrip()
        sn = inventory_device[2].replace("SN: ","").replace(" ", "").rstrip()
        print(f"PID: {pid}")
        print(f"VID: {vid}")
        print(f"SN: {sn}")
        
        ssh_client.connect(ip, username=SSH_USERNAME, password=SSH_PASSWORD)    # Connect to host
        ssh_in, ssh_out, ssh_err = ssh_client.exec_command("show version")              # Execute version command
        for line in ssh_out.readlines():
            line = line.rstrip()
            if not match(regex.EMPTY_LINE, line):   # Remove all empty lines from command output
                if match(regex.CISCO_IOS_VERSION, line):    # Match only usefull lines
                    version = line.split(",")[2].strip().rstrip().split(" ")[1]     # Take only the version number and build
        print(f"Version: {version}")

        ssh_client.close()

        # Format commands outputs into JSON
        json_host_output = {
                            "Hostname"  : hostname,
                            "IP"        : ip,
                            "PID"       : pid,
                            "VID"       : vid,
                            "SN"        : sn,
                            "Version"   : version
        }
        # Append results to JSON output array
        hosts_out.append(json_host_output)

        # Separate hosts
        print("-" * 40)

    except AuthenticationException:
        print("AuthenticationException")
        print("Exiting to avoid user locks")
        break

    except BadHostKeyException:
        print("BadHostKeyException")
        print("Exiting")
        break

    except SSHException:
        print("SSHException")
        print("Exiting")
        break
    
    finally:
        ssh_client.close()

# Write all hosts' data into JSON file
with open("out.json", "w") as output:
    output.write(json.dumps(hosts_out))