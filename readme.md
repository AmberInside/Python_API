# Python API

This repository provides templates for the development of the Python examples based on the AMBER UDP protocol, the number in the file name is the command number in UDP protocol.

UDP protocol link：https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing .

## First-Time Users

We recommend you getting started with  [cmd_04_single_move.py](https://github.com/Muya369/Python_API/blob/main/cmd_04_single_move.py) ,which allows you control multiple joint to move once by input their position ( unit of angle: rad, 1rad   ≈ 57.296° ) .

Make sure you have read our [UDP protocol](https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing) .

#### Set IP address

Set your ROS Master's  `IP_ADDR ` in [Line 11](https://github.com/Muya369/Python_API/blob/main/cmd_04_single_move.py#L11) .

#### Data structures(Ctype structure)

We will explain these later.

We use Python `ctypes` structure to make everything matches C++ API, so `c_uint16` == `uint16_t` in protocol .

`_pack_ = 1` is for override structure align, no need to change in normal situation.

#### Prepare socket connection

```python
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               
s.bind(("0.0.0.0", 12321))
```

These are standard socket processes, no need to change in normal situation.

#### Prepare control data

Modify position and angles in in [Line 42](https://github.com/Muya369/Python_API/blob/main/cmd_04_single_move.py#L42) :

from

```python
payloadS = robot_joint_position(4, 44, 114514,0,0,0,0,0,0,0,0,1)
```

to

```python
payloadS = robot_joint_position(4, 44, 114514,0,0,0,1.57,0,-1.57,0,0,1)
```

| Type     | Data    | Example | Comment                                                      |
| -------- | ------- | ------- | ------------------------------------------------------------ |
| c_uint16 | cmd_no  | 4       | Command Number, 4 :  Single Joint move once                  |
| c_uint16 | length  | 44      | Length, 44 , Fixed value for Command 4                       |
| c_uint32 | counter | 114514  | Correspondence code, you can choose any number you like      |
| c_float  | pos0    | 0       | Joint 1 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos1    | 0       | Joint 2 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos2    | 0       | Joint 3 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos3    | 1.57    | Joint 4 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos4    | 0       | Joint 5 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos5    | -1.57   | Joint 6 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos6    | 0       | Joint 7 target position, use radian measure, 1 rad ≈ 57.296° |
| c_float  | pos7    | 0       | Joint target position, which may use in future , irrelevant right now |
| c_float  | time    | 1       | Duration time to target, from current position to next position |

#### Send data by socket

```python
s.sendto(payloadS, (IP_ADDR, 25001))
```

Default port is 25001, no need to change in normal situation.

**If everything is set up correctly, when you send these data by socket, joint 4 and joint 6 will rotate 90°(and -90° for joint 6), make sure the robot workspace is clear.**

#### Prepare receive data from socket

```python
data, addr = s.recvfrom(1024) 
print("Receiving: ", data.hex())
```

You will see raw data printed out in terminal, and you can easily convert raw data into ctypes struct and print out in terminal .

```python
payloadR = robot_mode_data.from_buffer_copy(data)
print("Received: cmd_no={:d}, length={:d}, "
      "counter={:d}, respond={:d}".format(payloadR.cmd_no,
                                          payloadR.length,
                                          payloadR.counter,
                                          payloadR.respond, ))
```

| Type     | Data    | Example | Comment                      |
| -------- | ------- | ------- | ---------------------------- |
| c_uint16 | cmd_no  | 4       | Command Number, 4            |
| c_uint16 | length  | 9       | Length, 9, Fixed value       |
| c_uint32 | counter | 114514  | Correspondence code          |
| c_uint8  | respond | 1       | Flag, 0: Failure，1: Success |

#### Terminal output for example

```bash
Sending: cmd_no=4, length=44, counter=114514,
pos0=0.000000,pos1=0.000000,pos2=0.000000,pos3=1.570000,pos4=0.000000,pos5=-1.570000,pos6=0.000000,pos7=0.000000,time=1.000000
Receiving:  0400090052bf010001
Received: cmd_no=4, length=9, counter=114514, respond=1
```

