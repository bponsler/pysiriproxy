#!/bin/bash
# Copyright (C) 2012 Brett Ponsler
# This file is part of pysiriproxy.
#
# pysiriproxy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysiriproxy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysiriproxy.  If not, see <http://www.gnu.org/licenses/>.
#
# Set the dnsmasq IP address to the given IP, and restart it to
# use the new settings.
# Author - Brett Ponsler, August 2012


# Set up the default values for command line argument values
GUZZONI_SERVER="guzzoni.apple.com"
KRYTEN_SERVER="kryten.apple.com"


# Create a function to print out the expected syntax for this script
function printSyntax {
    echo "Syntax: $0 [interface name]"
    echo "Options:"
    echo "    -h -- Display this information and exit."
}


# Parse the command line arguments
while getopts "h" opt; do
  case $opt in
    h)
      # Print the script syntax for help
      printSyntax $0
      exit 0
      ;;
    *)
      # Invalid option was given
      exit 2
      ;;
  esac
done

# Shift the arguments down to get the remaining arguments
shift $(( $OPTIND -1 ))

# Make sure the interface was given
if [ "$#" != "1" ]; then
    printSyntax
    exit 1
fi

# Check to ensure that the interface actually exists
ifconfig $1 &> /dev/null
if [[ $? != 0 ]]; then
    echo "ERROR: '$1' is not a valid interface name!"
    exit 2
fi

# Now attempt to get the IP address from the interface name
IP=`ifconfig $1 | grep inet | grep -v inet6 | cut -d ":" -f 2 | cut -d " " -f 1`

# Make sure we found an IP address
if [ -z "$IP" ]; then
    echo "ERROR: Failed to locate IP address for interface '$1'!"
    echo "Please ensure that the interface is properly configured and try again."
    exit 3
fi

# Stop dnsmasq
sudo /etc/init.d/dnsmasq stop >> /dev/null

# Create the lines to support both servers with the given IP address
guzzoniLine="address=/$GUZZONI_SERVER/$IP"
krytenLine="address=/$KRYTEN_SERVER/$IP\n"

# Replace the 62nd and 63rd line in the dnsmasq configuration file with
# the new line data using the new IP address
sudo sed -i "62c ${guzzoniLine}" /etc/dnsmasq.conf
sudo sed -i "63c ${krytenLine}" /etc/dnsmasq.conf

echo "Using Apple server: $APPLE_SERVER"
echo "Set dnsmasq IP to: $IP"

# Start dnsmasq
sudo /etc/init.d/dnsmasq start >> /dev/null
echo "dnsmasq has been restarted with the new IP."