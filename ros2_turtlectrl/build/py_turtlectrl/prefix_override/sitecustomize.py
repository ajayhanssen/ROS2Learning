import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/andi/Desktop/ROS2Learning/ros2_turtlectrl/install/py_turtlectrl'
