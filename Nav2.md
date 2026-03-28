# Nav2 Learning

## Turtlebot3
Gazebo is for running simulations. Use:
~~~
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
~~~
To run a turtlebot simulation.

The robot in the simulation can be controller via keyboard using:
~~~
ros2 run  turtlebot3_teleop teleop_keyboard 
~~~
To create a map using the simulated LIDAR sensor on top of the turtlebot, use the following command:
~~~
ros2 launch turtlebot3_cartographer  cartographer.launch.py use_sim_time:=True
~~~
to open the cartographer in RViz. Moving around creates a map of the surroundings step by step. To save a map, use:
~~~
ros2 run nav2_map_server map_saver_cli -f maps/my_map
~~~
This saves the map opened to a *my_map.yaml* and a *my_map.pgm* file.

## Map
*.yaml* file contains resolution in m, and other info like thresholds. To prevent issues when loading maps later, install:
~~~
sudo apt install ros-humble-rmw-cyclonedds-cpp
~~~
and put
~~~
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
~~~
into *.bashrc*

Start the navigation using:
~~~
ros2 launch turtlebot3_navigation2  navigation2.launch.py use_sim_time:=True map:=maps/my_map.yaml
~~~