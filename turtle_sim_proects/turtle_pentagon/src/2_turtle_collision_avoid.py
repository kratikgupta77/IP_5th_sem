#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.msg import Pose
import math

# Global variables for turtle poses
turtle1_pose = None
turtle2_pose = None

# Threshold distance for collision detection
threshold_distance = 3
def update_turtle1_pose(data):
    global turtle1_pose
    turtle1_pose = data

def update_turtle2_pose(data):
    global turtle2_pose
    turtle2_pose = data

def euclidean_distance(pose1, pose2):
    return math.sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2)

def move_turtles(radius):
    global turtle1_pose, turtle2_pose
    
    # Create publishers for both turtles
    vel_pub1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)

    # Set a rate for the loop
    rate = rospy.Rate(10)

    # Define Twist messages for moving in circles
    vel_msg1 = Twist()
    vel_msg1.linear.x = 2.0  # Speed
    vel_msg1.angular.z = 2.0 / radius  

    vel_msg2 = Twist()
    vel_msg2.linear.x = 2.0  # Speed
    vel_msg2.angular.z = -2.0 / radius  

    while not rospy.is_shutdown():
        if turtle1_pose and turtle2_pose:
            # Publish velocity commands to both turtles
            vel_pub1.publish(vel_msg1)
            vel_pub2.publish(vel_msg2)

            # Check if the turtles are within the threshold distance
            distance = euclidean_distance(turtle1_pose, turtle2_pose)
            if distance < threshold_distance:
                rospy.loginfo("Turtles are too close.")

                # Stop both turtles
                vel_msg1.linear.x = 0
                vel_msg1.angular.z = 0
                vel_pub1.publish(vel_msg1)

                vel_msg2.linear.x = 0
                vel_msg2.angular.z = 0
                vel_pub2.publish(vel_msg2)

                break  
        rate.sleep()

if __name__ == '__main__':
    try:
        # Initialize the ROS node
        rospy.init_node('turtle_two_collision', anonymous=True)

        # Define the radius of the circle (half of the width of the Turtlesim screen)
        radius = 4.0

        # Spawn the turtles at opposite ends of the circle
        #spawn_turtles(radius)

        # Subscribe to the pose of each turtle
        rospy.Subscriber('/turtle1/pose', Pose, update_turtle1_pose)
        rospy.Subscriber('/turtle2/pose', Pose, update_turtle2_pose)

        # Move turtles and check for collisions
        move_turtles(radius)

    except rospy.ROSInterruptException:
        pass
