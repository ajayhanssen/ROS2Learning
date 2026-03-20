# ROS2Learning

## Workspace and Building

ROS workspace structure:

```
-ros2_ws  
    -src      containing packages, source files, etc  
    -build    folder generated after running *colcon build* in root of workspace  
    -install  folder generated after running *colcon build* in root of workspace, run *source install/setup.bash* to source built packages  
```

run Node using
~~~
ros2 run package_name executable
~~~

Check for dependencies before building using *colcon*:
~~~
rosdep install -i --from-path src --rosdistro humble -y
~~~
dependencies of packages are declared in the *package.xml* file.

Building using
~~~
colcon build --symlink-install
~~~
saves us from rebuilding everything just because of some small changes in a python script.

## Creating a Package
To create a new package using *ament*, got to *workspace/src* folder and run:
~~~
ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub
~~~
This gets created:

```
ros2_ws
    -src
        -py_pubsub
            -py_pubsub/
                -__init__.py
            -resource/
                -py_pubsub
            -test/
                -test_copyright.py
                -test_flake8.py
                -test_pep257.py
            -LICENSE
            -package.xml
            -setup.cfg
            -setup.py
```