#!/usr/bin/env python
# Shebang line specifying the script should be run using the Python interpreter.

import rospy
from geometry_msgs.msg import Twist
import time

def move_square():
    # Initialize the ROS node named 'move_husky_square'.
    # The 'anonymous=True' flag ensures that if multiple instances are run, each has a unique name.
    rospy.init_node('move_husky_square', anonymous=True)
    
    # Create a publisher to send velocity commands to the Husky robot.
    # '/husky_velocity_controller/cmd_vel' is the topic for velocity commands.
    # 'Twist' is the message type that includes linear and angular velocities.
    # 'queue_size=10' sets the size of the outgoing message queue.
    pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
    
    # Set the rate at which messages are published (10 Hz).
    rate = rospy.Rate(10)  # 10Hz
    
    # Initialize a Twist message object to hold velocity commands.
    move_cmd = Twist()
    
    # Loop four times to create four sides of a square.
    for _ in range(4):
        # === Move Forward ===
        
        # Set linear velocity in the x-direction to 1.0 m/s (forward speed).
        move_cmd.linear.x = 1.0  # 1 m/s forward speed
        # Ensure no angular velocity during forward movement.
        move_cmd.angular.z = 0.0
        # Log the action for debugging purposes.
        rospy.loginfo("Moving Forward")
        
        # Publish the forward movement command repeatedly to sustain movement.
        # Loop runs 50 times at 10Hz, resulting in 5 seconds of forward motion.
        for _ in range(50):
            pub.publish(move_cmd)  # Publish the current velocity command.
            rate.sleep()           # Sleep to maintain the loop rate.
        
        # === Rotate 90 Degrees ===
        
        # Stop linear movement to prepare for rotation.
        move_cmd.linear.x = 0.0
        # Set angular velocity to rotate the robot.
        # 1.57 radians ≈ 90 degrees. Divided by 2 to get ~0.785 rad/s (~45 degrees/sec).
        move_cmd.angular.z = 1.57 / 2  # 90 degrees in radians per second (~45 degrees/sec)
        # Log the rotation action.
        rospy.loginfo("Rotating")
        
        # Publish the rotation command repeatedly to sustain rotation.
        # Loop runs 50 times at 10Hz, resulting in 5 seconds of rotation.
        # Note: At 0.785 rad/s, 5 seconds would result in ~3.93 radians (~225 degrees),
        # which is more than the intended 90 degrees. Adjust the duration or angular speed as needed.
        for _ in range(50):
            pub.publish(move_cmd)  # Publish the current velocity command.
            rate.sleep()           # Sleep to maintain the loop rate.
    
    # === Stop the Robot After Completing the Square Path ===
    
    # Set both linear and angular velocities to zero to stop the robot.
    move_cmd.linear.x = 0.0
    move_cmd.angular.z = 0.0
    # Publish the stop command to ensure the robot halts.
    pub.publish(move_cmd)
    # Log the completion of the square path.
    rospy.loginfo("Completed Square Path")

if __name__ == '__main__':
    try:
        # Execute the move_square function when the script is run.
        move_square()
    except rospy.ROSInterruptException:
        # Handle ROS interrupt exceptions gracefully (e.g., when shutting down the node).
        pass


