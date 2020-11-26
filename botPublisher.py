#!/usr/bin/env python
#Publisher node

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def botPublisher():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.init_node('botPublisher', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        move = 0

        msg = Twist()
        #Stop
        if move == 0:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        #Move forward
        if move == 1:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
        #Rotate left
        if move == 2:
            msg.linear.x = 0.0
            msg.angular.z = 1.0
        #Rotate right
        if move == 3:
            msg.linear.x = 0.0
            msg.angular.z = -1.0
        #Move backwards
        if move == 4:
            msg.linear.x = -0.5
            msg.angular.z = 0.0

        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        botPublisher()
    except rospy.ROSInterruptException:
        pass
