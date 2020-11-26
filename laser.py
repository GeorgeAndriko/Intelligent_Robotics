#!/usr/bin/env python
#Publisher node

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def clbk_laser(msg):
	#Our laser sensor sends 500 values for -pi/2 to pi/2
	#So, I divided that data to 5, every part represents indicates a direction. Ranges are given below.
    regions = {
        'right':  min(min(msg.ranges[0:99]), 10),
        'fright': min(min(msg.ranges[100:199]), 10),
        'front':  min(min(msg.ranges[200:299]), 10),
        'fleft':  min(min(msg.ranges[300:399]), 10),
        'left':   min(min(msg.ranges[400:499]), 10),
    }
    take_action(regions)


def take_action(regions):
    move = Twist()
    linear_x = 0
    angular_z = 0

    state_description = ''

    if regions['front'] >= 0.5 and regions['fleft'] >= 0.5 and regions['fright'] >= 0.5:
        state_description = 'case 1 - nothing'
        linear_x = 0.6
        angular_z = 0
    elif regions['front'] < 0.5 and regions['fleft'] >= 0.5 and regions['fright'] >= 0.5:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] >= 0.5 and regions['fleft'] >= 0.5 and regions['fright'] < 0.5:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] >= 0.5 and regions['fleft'] < 0.5 and regions['fright'] >=0.5:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 0.5 and regions['fleft'] >= 0.5 and regions['fright'] < 0.5:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 0.5 and regions['fleft'] < 0.5 and regions['fright'] >=0.5:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 0.5 and regions['fleft'] < 0.5 and regions['fright'] < 0.5:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = -0.6
        angular_z = -0.3
    elif regions['front'] >= 0.5 and regions['fleft'] < 0.5 and regions['fright'] < 0.5:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0.6
        angular_z = 0
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    move.linear.x = linear_x
    move.angular.z = angular_z
    pub.publish(move)



def callback(msg):

   	global pub
	pub.publish(move)
rospy.init_node('check_obstacle')
sub=rospy.Subscriber('/base_scan',LaserScan,clbk_laser)  # getting laser value and call clbk_laser function
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
move=Twist()
rospy.spin()


if __name__ == '__callback__':
    callback(msg)
