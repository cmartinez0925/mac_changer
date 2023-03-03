#!/usr/bin/python3

import subprocess
import argparse
import re
import MAC_Utils

mac_utils = MAC_Utils.MAC_Changer()

# Get argument passed on command line
args = mac_utils.get_args()

# Get the original MAC Address of the interface
original_mac = mac_utils.get_current_mac(args.interface)
print(f"The current MAC address for {args.interface} is {original_mac}")

# Change MAC Address of interface to the new MAC address
mac_utils.change_mac_addr(args.interface, args.new_mac)
changed_mac = mac_utils.get_current_mac(args.interface)

# Check if the MAC Address was changed correctly
mac_changed_successfully = mac_utils.check_mac_changed(original_mac, changed_mac)
if mac_changed_successfully:
    print(f"[+] The MAC address for {args.interface} changed to {changed_mac}")
else:
    print(f"[-] MAC Address of {args.interface} is still {original_mac}")
