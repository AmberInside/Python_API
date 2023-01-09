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
                ]


class robot_mode_data(Structure):                                   # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("pos_1", c_float),
                ("pos_2", c_float),
                ("pos_3", c_float),
                ("pos_4", c_float),
                ("pos_5", c_float),
                ("pos_6", c_float),
                ("pos_7", c_float),
                ("pos_8", c_float),
                ("speed_1", c_float),
                ("speed_2", c_float),
                ("speed_3", c_float),
                ("speed_4", c_float),
                ("speed_5", c_float),
                ("speed_6", c_float),
                ("speed_7", c_float),
                ("speed_8", c_float),
                ("X_pos", c_float),
                ("Y_pos", c_float),
                ("Z_pos", c_float),
                ("Roll_pos", c_float),
                ("Pitch_pos", c_float),
                ("Yaw_pos", c_float),
                ("X_speed", c_float),
                ("Y_speed", c_float),
                ("Z_speed", c_float),
                ("Roll_speed", c_float),
                ("Pitch_speed", c_float),
                ("Yaw_speed", c_float),
                ("Arm_Angle", c_float),
                ]


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                # Standard socket processes
s.bind(("0.0.0.0", 12321))
payloadS = robot_joint_position(1, 44, 114514)          # Fill struct for send with numbers
s.sendto(payloadS, (IP_ADDR, 25001))                                # Default port is 25001
print("Sending: cmd_no={:d}, "
      "length={:d}, counter={:d},".format(payloadS.cmd_no,
                                          payloadS.length,
                                          payloadS.counter, ))

data, addr = s.recvfrom(1024)                                       # Need receive return
print("Receiving: ", data.hex())
payloadR = robot_mode_data.from_buffer_copy(data)                   # Convert raw data into ctypes struct to print
print("Received: cmd_no={:d}, length={:d}, counter={:d}"
      .format(payloadR.cmd_no, payloadR.length, payloadR.counter))
print("pos1={:f} pos2={:f} pos3={:f} pos4={:f} pos5={:f} pos6={:f} pos7={:f} pos8={:f}"
      .format(payloadR.pos_1, payloadR.pos_2, payloadR.pos_3, payloadR.pos_4
              , payloadR.pos_5, payloadR.pos_6, payloadR.pos_7, payloadR.pos_8,))
print("speed1={:f} speed2={:f} speed3={:f} speed4={:f} speed5={:f} speed6={:f} speed7={:f} speed8={:f}"
      .format(payloadR.speed_1, payloadR.speed_2, payloadR.speed_3, payloadR.speed_4
              , payloadR.speed_5, payloadR.speed_6, payloadR.speed_7, payloadR.speed_8,))
print("X_pos={:f} Y_pos={:f} Z_pos={:f} R_pos={:f} P_pos={:f} Yaw_pos={:f} X_speed={:f} Y_speed={:f} Z_speed={:f} "
      "Roll_speed={:f} Pitch_speed={:f} Yaw_speed={:f} Arm_Angle={:f}"
      .format(payloadR.X_pos, payloadR.Y_pos, payloadR.Z_pos, payloadR.Roll_pos, payloadR.Pitch_pos,
              payloadR.Yaw_pos, payloadR.X_speed, payloadR.Y_speed, payloadR.Z_speed, payloadR.Roll_speed,
              payloadR.Pitch_speed,payloadR.Yaw_speed, payloadR.Arm_Angle))
