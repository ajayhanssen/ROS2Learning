#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node

# import message type "String", other are "Pose", "Twist", "Quaternion", ...
from std_msgs.msg import String
#-------------------------------------------------------------------------------#
# THese dependencies ^ need to be added to "package.xml" !!


# Pub Node setup, inehrit from "Node"
#-------------------------------------------------------------------------------#
class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher') # Call Node-constructor, "minimal_publisher" is the Node-name
        self.publisher_ = self.create_publisher(String, 'topic', 10) # create Publisher as a member of the class object. (msg_type, topic, queue_size)
        # Queue size is a required setting and limits the amount of queued messages if a subscriber does not read fast enough.

        timer_period = 0.5 # secondas
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        if self.i % 10 == 0:
            msg.data = f"Hello Huansohn: {self.i}"
        else:
            msg.data = f"Hello World: {self.i}"

        self.publisher_.publish(msg)
        self.get_logger().info(f"Han grad -{msg.data}- gschickt.")
        self.i += 1
#-------------------------------------------------------------------------------#


# Main function, spinning the node an destroying after use
#-------------------------------------------------------------------------------#
def main(args=None):
    rclpy.init(args=args)

    minimal_publinger = MinimalPublisher()

    rclpy.spin(minimal_publinger)


    minimal_publinger.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()