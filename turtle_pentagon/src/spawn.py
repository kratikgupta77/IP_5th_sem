#!/usr/bin/env python3
import rospy
from turtlesim.srv import Spawn

def spawn_turtle():
    rospy.init_node('spawn_turtle', anonymous=True)

    rospy.wait_for_service('/spawn')
    try:
        spawn_turtle = rospy.ServiceProxy('/spawn', Spawn)
        
        spawn_turtle(5,5, 0, 'turtle2')
        rospy.loginfo("Spawned turtle2 at (5, 5)")
    except rospy.ServiceException as e:
        rospy.loginfo(f"Service call failed: {e}")

if __name__ == '__main__':
    spawn_turtle()
