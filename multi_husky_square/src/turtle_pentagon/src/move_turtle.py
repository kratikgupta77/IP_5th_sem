#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
import time

class HuskyMover:
    def __init__(self, husky_ns):
        self.husky_ns = husky_ns
        self.pub = rospy.Publisher(f'/{self.husky_ns}/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pattern = 0  # 0 for square, 1 for rhombus
        self.position_dict = {
            0: {'husky_1': (0, 0), 'husky_2': (2, 0), 'husky_3': (2, 2), 'husky_4': (0, 2)},  # Square formation
            1: {'husky_1': (1, 0), 'husky_2': (2, 1), 'husky_3': (1, 2), 'husky_4': (0, 1)}   # Rhombus formation
        }

    def move_husky(self):
        """Move the Husky to its position based on the current formation."""
        move_cmd = Twist()

        # Get the position for the current formation
        if self.husky_ns == "husky_1":
            x, y = self.position_dict[self.current_pattern]["husky_1"]
        elif self.husky_ns == "husky_2":
            x, y = self.position_dict[self.current_pattern]["husky_2"]
        elif self.husky_ns == "husky_3":
            x, y = self.position_dict[self.current_pattern]["husky_3"]
        elif self.husky_ns == "husky_4":
            x, y = self.position_dict[self.current_pattern]["husky_4"]

        # Move Huskies based on the formation's desired coordinates
        move_cmd.linear.x = 0.5  # Move forward at a constant speed
        move_cmd.linear.y = 0.0  # Stay on the current Y-axis (no lateral movement)
        move_cmd.angular.z = 0.0  # No turning (just linear movement)

        rospy.loginfo(f"Moving {self.husky_ns} to position {x}, {y}")
        self.pub.publish(move_cmd)
        self.rate.sleep()

    def switch_formation(self, req):
        """Switch between square and rhombus formation."""
        rospy.loginfo(f"Switching formation for {self.husky_ns}")
        self.current_pattern = 1 if self.current_pattern == 0 else 0
        return TriggerResponse(success=True, message=f"Formation switched for {self.husky_ns}")


if __name__ == '__main__':
    try:
        rospy.init_node('husky_mover', anonymous=True)

        husky_ns = rospy.get_param("~husky_ns")  # Get the namespace parameter
        mover = HuskyMover(husky_ns)

        # Initialize the service to switch formation
        rospy.Service(f'/{husky_ns}/switch_formation', Trigger, mover.switch_formation)

        # Move the Husky to the starting position
        while not rospy.is_shutdown():
            mover.move_husky()

    except rospy.ROSInterruptException:
        pass
