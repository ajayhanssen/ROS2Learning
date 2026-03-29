#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node

# import message type "String", other are "Pose", "Twist", "Quaternion", ...
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

import numpy as np
#-------------------------------------------------------------------------------#
# THese dependencies ^ need to be added to "package.xml" !!

class simplePose:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

# Pub Node setup, inehrit from "Node"
#-------------------------------------------------------------------------------#
class PurePursuit(Node):
    def __init__(self):
        super().__init__('pure_pursuit_node') # NOde name, call Node constructor

        # params
        self.look_ahead_distance = 0.1
        self.linear_vel = 0.11

        # test path (Max aktiv)
        self.path = [(0.25, 0.25), (0.5, 1.0), (1.0, 0.75), (0.75, 0.5), (1.0, 0.25)]
        self.target_idx =  0

        # publisher and subscriber member for Pose and Twist of turtles
        self.publisher_ = self.create_publisher(Twist, '/my_robot/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/my_robot/odom', self.pose_callback, 10)


    def pose_callback(self, msg):
        point = msg.pose.pose.position
        orient_q = msg.pose.pose.orientation
        orient_list = [orient_q.x, orient_q.y, orient_q.z, orient_q.w]

        (roll, pitch, yaw) = euler_from_quaternion(orient_list)
        
        pose = simplePose(point.x, point.y, yaw)


        # 1) find target waypoint
        self.update_target(pose)
        target_x, target_y = self.path[self.target_idx]

        # 2) transform target to turtlinger coords

        dx = target_x - pose.x
        dy = target_y - pose.y

        # hom rot mat
        y_local = -dx * np.sin(pose.theta) + dy * np.cos(pose.theta)

        # 3) pure pursuit algo
        # curvature gamma = 2 * y_local / L^2
        curvature = (2 * y_local) / (self.look_ahead_distance**2)

        # 4) publish twist
        cmd = Twist()
        cmd.linear.x = self.linear_vel
        
        max_ang = 2.0  # rad/s
        cmd.angular.z = np.clip(self.linear_vel * curvature, -max_ang, max_ang)
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