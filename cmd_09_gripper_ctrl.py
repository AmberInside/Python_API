import socket
from ctypes import *

'''
A simple example for controlling a single joint move once by python

Ref: https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing#2-single-joint-move-once
C++ version:  https://github.com/MrAsana/C_Plus_API/tree/master/amber_gui_4_node
     
'''
IP_ADDR = "192.168.51.27"                                           # ROS master's IP address


class robot_joint_position(Structure):                              # ctypes struct for send
    _pack_ = 1                                                      # Override Structure align
    _fields_ = [("cmd_no", c_uint16),                               # Ref:https://docs.python.org/3/library/ctypes.html
                ("length", c_uint16),
                ("counter", c_uint32),
                ("action", c_uint16),                               # Ref:https://docs.python.org/3/library/ctypes.html
                ("intensity", c_uint16),
                # ("version", c_bool)
                ]


class robot_mode_data(Structure):                                   # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("respond", c_uint8),
                ]


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                # Standard socket processes
s.bind(("0.0.0.0", 12321))
payloadS = robot_joint_position(9, 12, 114514,0,10)
s.sendto(payloadS, (IP_ADDR, 25001))                                # Default port is 25001
print("Sending: cmd_no={:d}, "
      "length={:d}, counter={:d},".format(payloadS.cmd_no,
                                          payloadS.length,
                                          payloadS.counter, ))

print("Action={:d},Intensity={:d},Version={:d}".format(payloadS.action, payloadS.intensity, payloadS.intensity))

data, addr = s.recvfrom(1024)                                       # Need receive return
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)                   # Convert raw data into ctypes struct to print
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))
