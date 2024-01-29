import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose

class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')

        # Current pose subscriber
        self.gt_pose_sub = self.create_subscription(
            Pose,
            '/drone/gt_pose',
            self.pose_callback,
            1)

        self.gt_pose = None

        # Control command publisher
        self.command_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)

        # Parameters for square path
        self.square_side_length = 2.0  
        self.linear_speed = 0.2  
        self.angular_speed = 0.5  

        # Callback for executing control commands
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Initialize variables for square path
        self.target_pose = Pose()
        self.target_pose.position.x = 0.0
        self.target_pose.position.y = 0.0
        self.target_pose.orientation.z = 0.0
        self.state = "move_forward"

    def pose_callback(self, data):
        self.gt_pose = data
        print(f"Current pose: {self.gt_pose}")

    def timer_callback(self):
        if self.gt_pose is not None:
            if self.state == "move_forward":
                
                if self.gt_pose.position.x < self.target_pose.position.x + self.square_side_length:
                    cmd_vel = Twist()
                    cmd_vel.linear.x = self.linear_speed
                    self.command_pub.publish(cmd_vel)
                else:
                    
                    self.state = "turn_right"
                    self.target_pose.orientation.z += 90.0  # 90 degrees

            elif self.state == "turn_right":
              
                if self.gt_pose.orientation.z < self.target_pose.orientation.z:
                    cmd_vel = Twist()
                    cmd_vel.angular.z = self.angular_speed
                    self.command_pub.publish(cmd_vel)
                else:
                   
                    self.state = "move_forward"
                    self.target_pose.position.x = self.gt_pose.position.x

def main(args=None):
    rclpy.init(args=args)
    node = DroneController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

