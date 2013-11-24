'''
Created on 04.10.2012

@author: Albrecht Nitsche
'''

from serial import Serial
import serial

class SAAP(object):

        
    def __init__(self, portName, baudrate): 
        self.object = object
        self.portName = portName
        self.baudrate = baudrate
        self.handlers = {}
        # semicolon
        self.END_BYTE = b'\x3B'
        
    def __del__(self):
        pass
        
    def __str__(self):
        return "SAAP (port: " + self.portName + ", baudrate: " + str(self.baudrate) + ")"
        
    def connect(self):
        self.ser = Serial(port=self.portName, baudrate=self.baudrate, timeout=None, parity=serial.PARITY_NONE)
        
    def registerCommand(self, flag, function):
        self.handlers[flag] = function
        
    def __getCallbackFor(self, flag):
        return self.handlers[flag]
        
    def __hasCallbackFor(self, flag):
        return self.__getCallbackFor(flag) is not None
    
    def __applyCallback(self, msg):
        msgString = msg.decode()
        length = len(msgString);
        flag = msgString[0];
        #print("msg: " + msgString + " flag: " + flag);
        callback = self.__getCallbackFor(flag) 
        if(callback is not None):
            #print(msgString);
            callback(flag, msgString[1:length - 1])
        
          
    def send(self, flag, intValue):
       
        dataString = flag.decode() + str(intValue) + self.END_BYTE.decode()
        data = bytes(dataString, 'utf-8')
        self.ser.write(data)
        print("send: " + dataString)                   
        
        
    def receive(self):
        
        theSerial = self.ser
        count = 0
        incommingBytes = bytearray()
        
        if theSerial.inWaiting() > 0:
            
            msgComplete = False;
            
            while msgComplete is False:
                 byte = theSerial.read()
                 
                 count += 1
                 
                 incommingBytes.append(ord(byte))
                 if byte == self.END_BYTE:
                     self.__applyCallback(incommingBytes)
                     count = 0
                     msgComplete = True


