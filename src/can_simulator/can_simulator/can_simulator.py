import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import String
from wuta_msgs.msg import MissionState


class CANBusSimulator(Node):
    def __init__(self):
        super().__init__('can_simulator')

        self.twist_pub = self.create_publisher(
            TwistStamped, '/localization/velocity', 50)

        self.gt_sub = self.create_subscription(
            Odometry, '/sim/ground_truth',
            self.ground_truth_callback, 50)

        self.mission_state_sub = self.create_subscription(
            MissionState, '/system/mission_state',
            self.mission_state_callback, 10)

        self.inspection_result_sub = self.create_subscription(
            String, '/system/inspection_result',
            self.inspection_result_callback, 10)

        self.get_logger().info(
            'can_simulator started: /sim/ground_truth -> /localization/velocity')

    def ground_truth_callback(self, msg: Odometry):
        twist = TwistStamped()
        twist.header.stamp = msg.header.stamp
        twist.header.frame_id = 'base_link'
        twist.twist.linear.x = msg.twist.twist.linear.x
        twist.twist.linear.y = msg.twist.twist.linear.y
        twist.twist.linear.z = msg.twist.twist.linear.z
        twist.twist.angular.x = msg.twist.twist.angular.x
        twist.twist.angular.y = msg.twist.twist.angular.y
        twist.twist.angular.z = msg.twist.twist.angular.z
        self.twist_pub.publish(twist)

    def mission_state_callback(self, msg: MissionState):
        state_names = {
            MissionState.IDLE: 'IDLE',
            MissionState.READY: 'READY',
            MissionState.INSPECTION: 'INSPECTION',
            MissionState.EXPLORE: 'EXPLORE',
            MissionState.MAPPING_DONE: 'MAPPING_DONE',
            MissionState.RACE: 'RACE',
            MissionState.FINISH: 'FINISH',
            MissionState.EMERGENCY: 'EMERGENCY',
        }
        mode_names = {
            MissionState.MISSION_TRACKDRIVE: 'TRACKDRIVE',
            MissionState.MISSION_SKIDPAD: 'SKIDPAD',
            MissionState.MISSION_ACCELERATION: 'ACCELERATION',
        }
        state_name = state_names.get(msg.state, 'UNKNOWN')
        mode_name = mode_names.get(msg.mission_mode, 'UNKNOWN')
        self.get_logger().debug(
            'Mission state: %s, mode: %s', state_name, mode_name)

    def inspection_result_callback(self, msg: String):
        self.get_logger().info(
            'Inspection result: %s', msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = CANBusSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down can_simulator...')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
