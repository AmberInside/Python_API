import socket
import time
from ctypes import *
IP_ADDR = "192.168.137.2"                                           # ROS master's IP address


class robot_joint_position(Structure):                              # ctypes struct for send
    _pack_ = 1                                                      # Override Structure align
    _fields_ = [("cmd_no", c_uint16),                               # Ref:https://docs.python.org/3/library/ctypes.html
                ("length", c_uint16),
                ("counter", c_uint32),
                ]


class robot_mode_data(Structure):                                   # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("respond", c_uint8),
                ]


tmp_req = robot_mode_data()
tmp_req.cmd_no = 2
tmp_req.length = 8

tmp_2_req = robot_mode_data()
tmp_2_req.cmd_no = 3
tmp_2_req.length = 8

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 12321))
s.sendto(tmp_req, (IP_ADDR, 25001))
data, addr = s.recvfrom(1024)
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))
time.sleep(5)

s.sendto(tmp_2_req, (IP_ADDR, 25001))
data, addr = s.recvfrom(1024)
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))

