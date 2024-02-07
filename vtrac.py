import os
import socket
import requests
import shutil
clear="cls"
def get_location(arg1):
    ip_address = arg1
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
        "country_area": response.get("country_area"),
        "timezone": response.get("timezone"),
        "country_calling_code": response.get("country_calling_code"),
        "org": response.get("org")
    }
    return location_data
def tshark(sec):
    cmd = f"tshark -i Wi-Fi -w packets.pcap -a duration:{sec}"
    os.system(cmd)
    print("\nFiltered Binding Request STUN Packets after scanning:\n\nSrc\t\t\t\tDest\t\t\tAttr Val")
    cmd = f"tshark -Y stun.type.method==0x001 -T fields -e ip.src -e ip.dst -e stun.attribute -r packets.pcap -w packets1.pcap"
    os.system(cmd)
    cmd = f"tshark -Y ip.dst!={ip_address} -T fields -e ip.src -e ip.dst -e stun.attribute -r packets1.pcap -w filteredPackets.pcap | sort /unique > filteredPackets.txt"
    os.system(cmd)
def Intro():
    os.system(clear)
    '''
    print("\n\t\t\t\tP A C K E T  P I C K E R S\n\n")
    print("\t\t\t\t\t  VoIP Tracer\n\n")
    print("\t  Tool under development - Only for Testing Purpose\n\n")
    '''
    print("\n")
    print("P A C K E T  P I C K E R S".center(shutil.get_terminal_size().columns))
    print("\n")
    print("VoIP Tracer".center(shutil.get_terminal_size().columns))
    print()
    print("Tool under development - Only for Testing Purpose\n\n".center(shutil.get_terminal_size().columns))

#getting host ip
hostname=socket.gethostname()
ip_address=socket.gethostbyname(hostname)

#start tracing
Intro()
print("[1]Start Tracing")
opt=int(input())
if opt==1:
    sec=int(input("Enter the Duration of the Scanning(in secs): "))
    tshark(sec)
    ch=input("\nWant to view all captured STUN Packets (y/n): ")
    filtFile = open("filteredPackets.txt", "r")
    packets = []
    try:
        for packet in filtFile.readlines():
            packets.append(packet.split())
    except:
        pass
    if packets:
        if ch=="y" or ch=="Y":
            Intro()
            print("\tAll VoIP Packets that have been captured\n\nSrc\t\tDest\t\tAttr Val\n---------------------------------------------------------------------------")
            cmd="tshark -Y stun -T fields -e ip.src -e ip.dst -e stun.attribute -r packets.pcap"
            os.system(cmd)
            buff=input("\n\tPress Enter to Continue")

        print("\n\n\t\t\tLoading....")

        if len(packets)>2:
            print("Warning: More than one users found in VoIP calling!, So just ignoring the other Packets other than 1st.")
        found_ip=[]
        for packet in packets:
            found_ip.append(packet[1])
        details=[]
        for ip in found_ip:
            details.append(get_location(ip))
        while True:
            Intro()
            print("\nObtained IP:\n")
            for i in range(len(found_ip)):
                print("["+str(i+1)+"] "+str(found_ip[i]))
            ipch=input("\nSelect ip for More Details\nPress 'q' to quit\n")
            if ipch=='q':
                break
            n=0
            try:
                n=int(ipch)
            except:
                pass
            if n <1 or n>len(found_ip):
                print("wrong Choice!! try Again")
            else:
                if details[n-1]:
                    Intro()
                    print("\t\tRetrieved Details of ["+str(n)+"]\n")
                    for data in details[n-1]:
                        print(str(data)+" : "+str(details[n-1][data]))
                else:
                    print("Private IP!! - No Data Retrieved")

            buff=input("\n\tPress Enter to go back to IP Menu")