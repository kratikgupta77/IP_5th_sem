#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import Int16

def numPublish():
    pub = rospy.Publisher('number_out', Int16, queue_size=3)
    rospy.init_node('int_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    hello_str = 1
    while not rospy.is_shutdown():
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        hello_str+=1
        rate.sleep()
        if (hello_str >1000):
            break

if __name__ == '__main__':
    try:
        numPublish()
    except rospy.ROSInterruptException:
        pass
