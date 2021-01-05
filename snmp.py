import subprocess as s
import ipaddress
import telnetlib
import os
import csv


total = []

portno=("161")
def pingIp(host):
    FNULL = open(os.devnull, 'w')
    if(s.call(["ping","-c1",host], stdout=FNULL, stderr=s.STDOUT)==0):
        return True
    else:
        return False
for host in ipaddress.IPv4Network('1.1.1.0/24'):
    host = str(host)
    if pingIp(host) is True:
        try:
            conn = telnetlib.Telnet((host), portno)
            response = (host)+':' + portno +' - ok pinging is work & -telnet- "Success"'
            T = {
                "ip": host,
                "ping": True,
                "telnet": True
            }
            total.append(T)
        except:
            response = (host)+':' + portno +' - ok pinging is work but -telnet- "Failed"'
            F = {
                "ip": host,
                "ping": True,
                "telnet": False
            }
            total.append(F)
        finally:
            print(response)
            
    else:
        N = {
            "ip": host,
            "ping": False,
            "telnet": False
        }
        total.append(N)
        print (host + " pinging doesn't work ")


keys = total[0].keys()
with open('example.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(total)
# print(total)
# print(Successful)
# print(badRequest)

