import socket
from ctypes import *
import time
'''
An example for Cartesian control by python

Ref: https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing#4-cartesian-control

'''

IP_ADDR = "192.168.50.32"                           # ROS master's IP address


class robot_joint_position(Structure):              # ctypes struct for send
    _pack_ = 1                                      # Override Structure align
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("xyz", c_float * 3),               # ctypes array
                ("rpy", c_float * 3),
                ("arm_angle", c_float),
                ("time", c_float),
                ]


class robot_mode_data(Structure):                   # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("respond", c_uint8),
                ]


tmp_1 = robot_joint_position()
tmp_1.cmd_no = 6
tmp_1.length = 40
tmp_1.xyz[1] = -0.0651
tmp_1.xyz[0] = 0.0
tmp_1.xyz[2] = 0.6499
tmp_1.rpy[0] = 0.035595                             # 弧度=57.29578 度
tmp_1.rpy[1] = -0.12545                             # 1 rad ≈ 57.296°
tmp_1.rpy[2] = -0.2592
tmp_1.arm_angle = 0.7
tmp_1.time = 4.0

tmp_2 = robot_joint_position()
tmp_2.cmd_no = 6
tmp_2.length = 40
tmp_2.xyz[0] = 0.2
tmp_2.xyz[1] = 0
tmp_2.xyz[2] = 0.60
tmp_2.rpy[2] = 0.0
tmp_2.time = 4.0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 12321))
s.sendto(tmp_1, (IP_ADDR, 25001))

data, addr = s.recvfrom(1024)
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))
time.sleep(6)
s.sendto(tmp_2, (IP_ADDR, 25001))
data, addr = s.recvfrom(1024)
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))

