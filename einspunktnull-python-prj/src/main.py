'''
Created on 04.10.2012

@author: Albrecht Nitsche
'''

from net.einspunktnull.saap import SAAP


def onGotPotiValue(flag,args):
    print("onGotPotiValue flag: "+flag +" arguments: "+args)


saap = SAAP("COM17", 115200)

saap.registerCommand("p", onGotPotiValue)


saap.connect()

while True:
    saap.receive();





