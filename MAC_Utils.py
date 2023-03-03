# Author: Chris Martinez
# Version: 1.0
# Date: 2 March 2023

"""Command Line Device MAC Changer.
This module changes the MAC Address for a specified interface that:
    - Handles an interface with no MAC Address
    - Handles command line args no provided or incomplete
    - Uses the modules: subprocess, argparse, re

Simple usage example below::

    mac_utils = MAC_Utils.MAC_Changer()
    args = mac_utils.get_args()
    mac_utils.change_mac_addr(args.interface, args.new_mac)

"""
import subprocess
import argparse
import re

class MAC_Changer:
    # ========================
    # Class Attributes
    # ========================


    # ========================
    # Constructors
    # ========================  
    def __init__(self):
        """No Arg Constructor"""
        pass

    # ========================
    # Methods
    # ========================
    def get_args(self):
        """Gets arguments from the command line: interface and new_mac
        returns them in the variable args
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--interface", dest="interface", help="Interface to be changed")
        parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address for the specified interface")
        args = parser.parse_args()

        if not args.interface:
            parser.error("[-] Must specifiy interface, use --help for more info")
        elif not args.new_mac:
            parser.error("[-] Must specifiy MAC address, use --help for more info")

        return args
    
    def change_mac_addr(self, interface, new_mac):
        """Changes the mac address of the specified interface"""
        print(f"[+] Changing the MAC address of {interface} to {new_mac}")
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.run(["ifconfig", interface, "up"])

    def get_current_mac(self, interface):
        """Parses the output of ifconfig and returns a string of the 
        mac address from the specified interface. Typically used to print to
        screen.

        If a mac address is unable to be parsed via regex, then throws a 
        AttributeError except and informs user via a string print to stdout
        """
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        ether_mac_results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

        try:
            return ether_mac_results.group(0)
        except AttributeError:
            print("[-] Could not locate a MAC address for specified interface")

    def check_mac_changed(self, original_mac, changed_mac):
        """Checks if mac address has been changed"""
        if original_mac == changed_mac:
            return False
        return True