import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy

QOS = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

class Pong(Node):
    def __init__(self):
        super().__init__('pong')
        self.pub = self.create_publisher(String, '/pong', QOS)
        self.create_subscription(String, '/ping', self.pub.publish, QOS)

rclpy.init(); rclpy.spin(Pong())
