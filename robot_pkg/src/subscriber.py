#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int16
#c=1
def callback(data):
    #global c
    number=data.data
    #number+=c
    #c+=1
    if number >= 1000:
        rospy.loginfo("Reached 1000. Shutting down...")
        rospy.signal_shutdown("Reached 100")
    print(number)
    
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("number_out", Int16, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
