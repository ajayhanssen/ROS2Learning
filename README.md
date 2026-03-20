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
                -publisher_member_function.py (Only after manually creating)
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

On how to write the python code, look at the src directory. The new python files containing the code go into the same directory as *\__init__.py*

All the needed dependencies need to be added into *package.xml*, right below **<license>**, like this:

~~~
<exec_depend>rclpy</exec_depend>
<exec_depend>numpy</exec_depend>
...
~~~

The next step is to create an **entry point**. This tells the compiler what function to call and what the name of the executable is. In *setup.py*, at **entry_points**:

~~~
entry_points={
        'console_scripts': [
            'talker = py_pubsub.publisher_member_function:main',
            'listener = py_pubsub.subscriber_member_function:main'
        ],
    },
~~~

Then run the *rosdep* command from above to check if dependencies are installed and build using *colcon*.