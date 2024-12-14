#!/usr/bin/env python3

import rospy
from std_srvs.srv import Trigger, TriggerResponse
from move_turtle import HuskyMover, husky_positions

class MovementService:
    def __init__(self):
        self.huskies = []
        for husky, target_position in husky_positions.items():
            self.huskies.append(HuskyMover(husky, target_position))

    def start_movement(self, req):
        rospy.loginfo("Movement started!")
        for husky in self.huskies:
            husky.move_husky()
        return TriggerResponse(success=True, message="Huskies are moving to their targets.")

if __name__ == '__main__':
    rospy.init_node('movement_service')
    service = MovementService()
    s = rospy.Service('/start_huskies_movement', Trigger, service.start_movement)
    rospy.spin()
