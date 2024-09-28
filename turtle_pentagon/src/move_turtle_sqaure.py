#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from random import randint
import math
direction =0
import rospy
import math
from geometry_msgs.msg import Twist

def move_turtle(vel_pub, charge):
    rate = rospy.Rate(50)
    vel_msg = Twist()
    
    while charge > 0 and not rospy.is_shutdown():
        vel_msg.linear.x = 1  
        vel_msg.angular.z = 0.0  
        rospy.loginfo("Moving straight")
        move_time = 2.0  
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < move_time:
            vel_pub.publish(vel_msg)
            rate.sleep()
        vel_msg.linear.x = 0.0
        vel_pub.publish(vel_msg)
        angular_speed = math.radians(35)  
        relative_angle = math.radians(90)  
        vel_msg.angular.z = angular_speed  
        rospy.loginfo("Turning left")
        rotate_time = relative_angle / angular_speed 
        start_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_time < rotate_time:
            vel_pub.publish(vel_msg)
            rate.sleep()
        vel_msg.angular.z = 0.0
        vel_pub.publish(vel_msg)
        charge -= 1
    
    rospy.loginfo("Charge ran out!")

if __name__ == '__main__':
    try:
        rospy.init_node('turtle_random_move', anonymous=True)
        vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        charge = 6
        move_turtle(vel_pub, charge)

    except rospy.ROSInterruptException:
        pass
