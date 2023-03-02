#!/usr/bin/env python

import subprocess # allows you to spawn new processes in your terminal
import optparse # parse CL arguments - allows you to define the options you want to accept and the values they should take and then parses the command line arguments.
import re #search for a pattern in a string
import random

def generate_mac(): #define 1st function
    mac = [ random.randint(0x00, 0x7f),
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac)) # lambda arguments : expression

def get_arguments():
    parser = optparse.OptionParser() #parse CL options and arguments
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    parser.add_option("-r", "--random", help="Randomly generate MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    return options


def change_mac(interface, new_mac=None):
    if new_mac is None or interface is None:
        new_mac = generate_mac()
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current Mac address is " + str(current_mac))
change_mac(options.interface, options.new_mac)
