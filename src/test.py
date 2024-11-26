import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import json

class ScanSaver(Node):
    def __init__(self):
        super().__init__('scan_saver')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.file_index = 0

    def scan_callback(self, msg):
        try:
            # Save scan data to a file
            filename = f'scan_data_{self.file_index}.json'
            with open(filename, 'w') as f:
                # Convert LaserScan message to a dictionary
                scan_data = {
                    'angle_min': msg.angle_min,
                    'angle_max': msg.angle_max,
                    'angle_increment': msg.angle_increment,
                    'time_increment': msg.time_increment,
                    'scan_time': msg.scan_time,
                    'range_min': msg.range_min,
                    'range_max': msg.range_max,
                    'ranges': list(msg.ranges),
                    'intensities': list(msg.intensities),
                }
                json.dump(scan_data, f, indent=4)

            self.get_logger().info(f'Scan data saved to {filename}')
            self.file_index += 1

        except Exception as e:
            self.get_logger().error(f'Failed to save scan data: {e}')


def main(args=None):
    rclpy.init(args=args)
    scan_saver = ScanSaver()

    try:
        rclpy.spin(scan_saver)
    except KeyboardInterrupt:
        pass
    finally:
        scan_saver.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
