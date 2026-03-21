#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node

# import message type "String", other are "Pose", "Twist", "Quaternion", ...
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import numpy as np
#-------------------------------------------------------------------------------#
# THese dependencies ^ need to be added to "package.xml" !!


# Pub Node setup, inehrit from "Node"
#-------------------------------------------------------------------------------#
class PurePursuit(Node):
    def __init__(self):
        super().__init__('pure_pursuit_node') # NOde name, call Node constructor

        # params
        self.look_ahead_distance = 1
        self.linear_vel = 1.5

        # test path (Max aktiv)
        self.path = [(5.0, 5.0), (3.0, 2.0), (2.0, 7.0), (10.0, 9.0), (7.0, 4.0)]
        self.target_idx =  0

        # publisher and subscriber member for Pose and Twist of turtles
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)


    def pose_callback(self, msg):
        # 1) find target waypoint
        self.update_target(msg)
        target_x, target_y = self.path[self.target_idx]

        # 2) transform target to turtlinger coords
        dx = target_x - msg.x
        dy = target_y - msg.y

        # hom rot mat
        y_local = -dx * np.sin(msg.theta) + dy * np.cos(msg.theta)

        # 3) pure pursuit algo
        # curvature gamma = 2 * y_local / L^2
        curvature = (2 * y_local) / (self.look_ahead_distance**2)

        # 4) publish twist
        cmd = Twist()
        cmd.linear.x = self.linear_vel
        cmd.angular.z = self.linear_vel * curvature
        self.publisher_.publish(cmd)

    def update_target(self, pose):
        # calcing distance from robot to current target point
        dist = np.sqrt((self.path[self.target_idx][0] - pose.x)**2 +
                       (self.path[self.target_idx][1] - pose.y)**2)
        
        # distance smasller than LAD, set new target
        if dist < self.look_ahead_distance and self.target_idx < len(self.path) - 1:
            self.target_idx += 1
        elif dist < self.look_ahead_distance and self.target_idx == len(self.path) - 1:
            self.target_idx = 0

#-------------------------------------------------------------------------------#


# Main function, spinning the node an destroying after use
#-------------------------------------------------------------------------------#
def main(args=None):

    rclpy.init(args=args)

    controller = PurePursuit()
    rclpy.spin(controller)


    controller.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()