import socket
from ctypes import *

'''

C++ version:  https://github.com/MrAsana/C_Plus_API/tree/master/amber_gui_20_node
     
'''

IP_ADDR = "192.168.137.2"


class state_point(Structure):
    _pack_ = 1
    _fields_ = [("sub_cmd_no", c_uint32),
                ("time", c_float),
                ("xyzrpya", c_float * 7)
                ]


class arc_point(Structure):
    _pack_ = 1
    _fields_ = [("sub_cmd_no", c_uint32),
                ("time", c_float),
                ("xyzrpya_a", c_float * 7),
                ("xyzrpya_b", c_float * 7)
                ]


class pause_point(Structure):
    _pack_ = 1
    _fields_ = [("sub_cmd_no", c_uint32),
                ("time", c_float)
                ]


class two_state(Structure):
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("cmd_num", c_uint32),
                ("a_point", state_point),
                ("b_point", pause_point),
                ("c_point", state_point)
                ]


class three_state(Structure):
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("cmd_num", c_uint32),
                ("a_point", arc_point),
                ("b_point", pause_point),
                ("c_point", state_point)
                ]


class robot_mode_data(Structure):
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("respond", c_uint8),
                ]


TS = three_state()
TS.cmd_no = 20
TS.length = 120
TS.cmd_num = 3

TS.a_point.sub_cmd_no = 3
TS.a_point.xyzrpya_a[0] = 0.0
TS.a_point.xyzrpya_a[1] = 0.0
TS.a_point.xyzrpya_a[2] = 0.72
TS.a_point.xyzrpya_a[3] = 0
TS.a_point.xyzrpya_a[4] = 0.0
TS.a_point.xyzrpya_a[5] = 0.0
TS.a_point.xyzrpya_a[6] = 0.0
TS.a_point.time = 8
TS.a_point.xyzrpya_b[0] = 0.0
TS.a_point.xyzrpya_b[1] = 0.2
TS.a_point.xyzrpya_b[2] = 0.45
TS.a_point.xyzrpya_b[3] = 0.0
TS.a_point.xyzrpya_b[4] = 0.0
TS.a_point.xyzrpya_b[5] = 0.0
TS.a_point.xyzrpya_b[6] = 0.0
TS.b_point.sub_cmd_no = 4
TS.b_point.time = 4
TS.c_point.sub_cmd_no = 2
TS.c_point.xyzrpya[0] = 0.0
TS.c_point.xyzrpya[1] = 0.0
TS.c_point.xyzrpya[2] = 0.65
TS.c_point.xyzrpya[3] = 0.0
TS.c_point.xyzrpya[4] = 0.0
TS.c_point.xyzrpya[5] = 0.0
TS.c_point.xyzrpya[6] = 0.0
TS.c_point.time = 4

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 12321))
s.sendto(TS, (IP_ADDR, 25001))

data, addr = s.recvfrom(1024)
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))
