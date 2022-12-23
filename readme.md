# Python API

This repository provides templates for the development of the Python examples based on the AMBER UDP protocol, the number in the file name is the command number in UDP protocol.

UDP protocol link：https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing .



## First-Time Users

We recommend you getting started with  [cmd_04_single_move.py](https://github.com/Muya369/Python_API/blob/main/cmd_04_single_move.py) ,which allows you control multiple joint to move once by input their position ( unit of angle: rad, 1rad   ≈ 57.296° ) .

Set your ROS Master's  `IP_ADDR ` in [Line 11](https://github.com/Muya369/Python_API/blob/main/cmd_4_single_move.py#L11) .

Modify position and angles in in [Line 42](https://github.com/Muya369/Python_API/blob/main/cmd_4_single_move.py#L42) .

Make sure you have read our [UDP protocol](https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing) .

