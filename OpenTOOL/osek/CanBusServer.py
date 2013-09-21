"""/* Copyright(C) 2013, OpenOSEK by Fan Wang(parai). All rights reserved.
 *
 * This file is part of OpenOSEK.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * Email: parai@foxmail.com
 * Sourrce Open At: https://github.com/parai/OpenOSEK/
 */
"""
import socket
def CanBusServerUsage():
    print "Usage:"
    print "\t python CanBusServer.py --server port"
    print "Example: python CanBusServer.py --server 8000"

def CanBusServerTrace(msg):
    if(len(msg) != 17):
        print 'Error: length of msg is invalid!'
        return
    #get CanID
    canid =  (ord(msg[0])<<24)+(ord(msg[1])<<16)+(ord(msg[2])<<8)+(ord(msg[3]))
    # get Port
    port = (ord(msg[13])<<24)+(ord(msg[14])<<16)+(ord(msg[15])<<8)+(ord(msg[16]))
    dlc = ord(msg[4])
    cstr = 'ID=%s, DLC=%s: ['%(hex(canid),dlc)
    for i in range(0,8):
        cstr += '%s, '%(hex(ord(msg[5+i])))
    cstr += ']'
    cstr += '...['
    for i in range(0,8):
        if(i<dlc):
            cstr += '%s, '%(msg[5+i])
        else:
            cstr += '., '
    cstr += '] From %s'%(port)
    print cstr

def CanBusServerForward(msg,port = 8000):
    """Forward msg received from one node to others connected to this server, exclude address."""
    # get Port
    portR = (ord(msg[13])<<24)+(ord(msg[14])<<16)+(ord(msg[15])<<8)+(ord(msg[16]))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for p in range(port+1,port+32):
        try: # only 31 nodes supported on one can bus.
            sock.connect(('127.0.0.1', p))  
            sock.send(msg)
        except:
            # print 'Invalid Port ', p
            continue  
    sock.close()

def CanBusServerHost(port = 8000):  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.bind(('127.0.0.1', port))  
    sock.listen(32)  
    while True:  
        connection,address = sock.accept()  
        try:  
            connection.settimeout(5)  
            msg = connection.recv(1024) 
            CanBusServerTrace(msg)
            CanBusServerForward(msg);           
        except socket.timeout:  
            continue  
        connection.close()

def CanBusServer(argc,argv):
    if(argc != 3):
        CanBusServerUsage()
        return
    if(argv[1] == '--server'):
        CanBusServerHost(int(argv[2]))
    
if __name__ == '__main__': 
    import sys 
    CanBusServer(len(sys.argv),sys.argv);