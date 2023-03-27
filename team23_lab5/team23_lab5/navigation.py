import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action._navigate_to_pose import NavigateToPose_FeedbackMessage
import numpy as np
import time
import sys




class GoalObject(Node):

    def __init__(self):
        super().__init__('Lab5')

        self.goals = np.array([[1.49,2.77,3.99], [0.34,-1.06,-0.85]])
        print(self.goals)
        self.i = 0
        print(self.goals[0, self.i], self.goals[1, self.i])

        self.waypoint = PoseStamped()
        self.waypoint.header.frame_id = 'map_lab5_tofunmi'
        self.waypoint.pose.position.x = self.goals[0, self.i]
        self.waypoint.pose.position.y = self.goals[1, self.i]
        self.waypoint.pose.position.z = 0.0
        self.waypoint.pose.orientation.x = 0.0
        self.waypoint.pose.orientation.y = 0.0
        self.waypoint.pose.orientation.z = 0.0
        self.waypoint.pose.orientation.w = 1.0

        # Declare publisher to goal_pose topic
        self.pose_publish = self.create_publisher(PoseStamped,'/goal_pose',10)
        self.pose_publish  # prevent unused variable warning

        self.pose_publish.publish(self.waypoint)

        # Declare subscriber to feedback message
        self.position_subscriber = self.create_subscription(NavigateToPose_FeedbackMessage, '/navigate_to_pose/_action/feedback', self.listener_callback, 10)
        self.position_subscriber  # prevent unused variable warning

        self.pose_publish.publish(self.waypoint)
        print('hey')

        goal_time = 1.0
        self.timer = self.create_timer(goal_time, self.timer_callback)


    def listener_callback(self, msg):
        if msg.feedback.distance_remaining < 0.1 and self.i < 2:
            self.i = self.i + 1
            print(self.i,self.goals[0, self.i], self.goals[1, self.i])
            print('next goal')
            self.waypoint = PoseStamped()
            self.waypoint.pose.position.x = self.goals[0, self.i]
            self.waypoint.pose.position.y = self.goals[1, self.i]
            time.sleep(5)
        elif msg.feedback.distance_remaining < 0.2 and self.i == 2:
            print('end')
            time.sleep(5)
            print('end')
            sys.exit()
        self.waypoint = PoseStamped()
        self.waypoint.pose.position.x = self.goals[0, self.i]
        self.waypoint.pose.position.y = self.goals[1, self.i]

        self.pose_publish.publish(self.waypoint)

    def timer_callback(self):
        print('timing')
        self.pose_publish.publish(self.waypoint)


def main(args=None):
    rclpy.init(args=args)
    print("I'm here")
    minimal_goal = GoalObject()

    rclpy.spin(minimal_goal)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    print("hello?")
    minimal_goal.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
