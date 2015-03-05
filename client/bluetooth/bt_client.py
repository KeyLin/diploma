import bluetooth
import uuid 


target_name = ""

def find_partner():

    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        print bdaddr


def connect_device():
	'''
		use mac address to find device & use uuid to set socket connection
	'''
	
	bd_addr = "60:E7:01:FD:75:02"
	phone_uuid = 'e8587008-297a-4676-9fc6-cc8ee6fa097c'
#	phone_uuid = uuid.UUID('phone_uuid')
	service_match = []
	while not service_match:
	    service_match = bluetooth.find_service( uuid=phone_uuid,address = bd_addr)
       
	
	print service_match
	port = service_match[0]['port']
	
    	sock= bluetooth.BluetoothSocket( bluetooth.RFCOMM)
	sock.connect( (bd_addr,port) )
	while True:	
	    sock.send('hello,world')
	    msg = sock.recv(1000)
	    print msg
	sock.close()
'''
bd_addr = ""
port =1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect( (bd_addr,port) )
sock.send("hello!")
sock.close()

'''



if __name__ == "__main__":
    #find_partner()
    connect_device() 
