
# A Python program to scan a remote network

# Importing scapy.all to generate and send/recv packets using scapy module
from scapy.all import ICMP,IP,sr
# Importing regular expression to verify the input
import re

# Defining the scanning function
def scan(ip):

    # Putting eveything in a try block especially to catch KeyboardInterrupt
    try:

        # Generating the ICMP header with the id=1 to scan the network
        icmp_header = ICMP(id=1)

        # Generating the IP header specifying the destination IP as the requested subnet
        ip_header = IP(dst=subnet)

        # Combining the headers to form a request packet
        request = ip_header/icmp_header

        # Declaring an empty client list to collective responses on each iteration (this list will have duplicate entries)
        clients = []

        # Print a status message
        print("\nScanning in Progress ...")

        # Declaring a variable that will show progress
        bar = 0

        # Print initial progress bar with 0% progress
        print('\n\r[{0}{1}]'.format('#'*bar, '-'*(30-bar)) + ' ' + str(int(bar/30*100)) + '% ', end="")

        # for loop for calling sr() three times for robustness
        for packet in range(0,3):

            # Using sr() methong to send and receive ICMP packets
            # Using timeout=2 & retry=3 argument to try not to miss hosts
            # And collecting the responses in answered variable
            answered = sr(request, timeout=2, retry=3, verbose=False)[0]

            # Appending the responses in the above declared list (this will have duplicate entries)
            clients.append(answered)

            # Incrementing the progress variable to show the progress after each iteration
            bar += 10

            # Printing the progress bar after each iteration
            print('\r[{0}{1}]'.format('#'*bar, '-'*(30-bar)) + ' ' + str(int(bar/30*100)) + '% ', end="")

        # Print another status message after scan is completed
        print("\n\nFinished Scanning.\n")

        # Declaring another empty list to store ip & mac for eah hosts (this list will also have duplicate entries)
        client_list = []

        # A for loop to iterate through the sendrcvlist and refer each tuple
        for client in clients:

            # Another for loop to iterate through each tuple of the list
            for item in client:

                # Appending to the above created list to make a list of clients
                client_list.append(item[1].src)

        # Create another list to remove the duplicate entries from the above scan
        hosts = [i for n, i in enumerate(client_list) if i not in client_list[n + 1:]]

        # Finally return the processsed list containing IPs for each alive host
        return hosts

    # Handling user interrupt by printing the following & returning empty list
    except KeyboardInterrupt:
        print("\n\nScanning aborted by user.\n")
        return []

# Putting eveything in a try block especially to catch KeyboardInterrupt
try:

    # This is the first statement to get executed asking for input
    subnet = input("\nEnter a remote subnet to scan [For eg. 10.0.0.0/24]: ")

    # Validating the user input for any typo
    if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", subnet) == None:
        print("\nIncorrect subnet. Please check.\n")

    else:

        # Calling the scan function by passing the requested subnet & collecting list in clients
        clients = scan(subnet)

        # Checking if the scan result is not an empty list
        if clients:

            # Print status for Generating List
            print("Generating List.\n")

            # A wait for 2 secs because without it the output is too quick
            time.sleep(2)

            # Sorting the list based on host IPs
            clients.sort()

            # Printing the result in a legible format
            print(" Active IPs\n--------------------")

            # for loop to access each (host)item in the (clients)list
            for host in clients:

            	print(" " + host)

            print("--------------------\n")

        # if scan resulted in an empty list
        else:
            print("Scan result was empty.\n")

# Handling user interrupt by printing the following
except KeyboardInterrupt:
    print("\n\nAborted by user. Exiting program.\n")
