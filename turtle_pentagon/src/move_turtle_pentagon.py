#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
import math

def move_turtle(side_length):
    rospy.init_node('turtle_pentagon', anonymous=True)
    vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz
    vel_msg = Twist()
    angle = math.radians(108)
    move_time = side_length / 2.0  
    for i in range(5):
        vel_msg.linear.x = 2.0  
        vel_msg.angular.z = 0.0  

        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < move_time:
            vel_pub.publish(vel_msg)
            rate.sleep()

        vel_msg.linear.x = 0.0
        vel_pub.publish(vel_msg)
        vel_msg.angular.z = 1.5  
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < (angle / 1.5):
            vel_pub.publish(vel_msg)
            rate.sleep()
        vel_msg.angular.z = 0.0
        vel_pub.publish(vel_msg)
    vel_msg.linear.x = 0.0
    vel_msg.angular.z = 0.0
    vel_pub.publish(vel_msg)

if __name__ == '__main__':
    try:
        side_length = float(input("Enter the length of the pentagon sides: "))
        move_turtle(side_length)
    except rospy.ROSInterruptException:
        pass

