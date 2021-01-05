import subprocess as s
import ipaddress
import telnetlib
import os
import csv
from pysnmp.hlapi import *

total = []

def pingIp(ip):
    FNULL = open(os.devnull, 'w')
    if(s.call(["ping","-c1",ip], stdout=FNULL, stderr=s.STDOUT)==0):
        return True
    else:
        return False

def snmpCheck(snmp_ip):
    iterator = getCmd(SnmpEngine(),
                  CommunityData('example'),
                  UdpTransportTarget((snmp_ip, 161)),
                  ContextData(),
                  ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:  # SNMP engine errors
        print(errorIndication)
        return False
    else:
        if errorStatus:  # SNMP agent errors
            print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
            return False
        else:
            return True


        
for host in ipaddress.IPv4Network('1.1.1.0/24'):
    host = str(host)
    if pingIp(host) is True:
        if snmpCheck(host) is True:
            N = {
                "ip": host,
                "ping": True,
                "snmp": True
            }
            total.append(N)
        else:
            N = {
                "ip": host,
                "ping": True,
                "snmp": False
            }
            total.append(N)


keys = total[0].keys()
with open('ip.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(total)


