
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class CANBusSimulator(Node):
    def __init__(self):
        super().__init__('can_bus_simulator')

        # --- Publisher: output to localization velocity ---
        self.twist_pub = self.create_publisher(
            TwistStamped,
            '/localization/velocity',
            50
        )

        # --- Subscriber: receive ground truth and forward directly ---
        self.gt_sub = self.create_subscription(
            TwistStamped,
            '/sim/ground_truth',
            self.ground_truth_callback,
            50
        )

        self.get_logger().info('CAN Bus Simulator started: forwarding /sim/ground_truth -> /localization/velocity')

    def ground_truth_callback(self, msg: TwistStamped):
        speed = TwistStamped()
        speed.header.stamp = self.get_clock().now().to_msg()
        speed.header.frame_id = 'base_link'
        speed.twist.linear.x = msg.twist.linear.x
        speed.twist.linear.y = msg.twist.linear.y
        speed.twist.linear.z = msg.twist.linear.z
        speed.twist.angular.x = msg.twist.angular.x
        speed.twist.angular.y = msg.twist.angular.y
        speed.twist.angular.z = msg.twist.angular.z
        self.twist_pub.publish(speed)


def main(args=None):
    rclpy.init(args=args)
    node = CANBusSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down CAN Bus Simulator...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
