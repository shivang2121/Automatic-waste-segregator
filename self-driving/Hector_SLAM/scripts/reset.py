#! /usr/bin/env python

import rospy
from std_msgs.msg import String

def main():
    pub = rospy.Publisher('syscommand', String, queue_size = 10)
    rospy.init_node('reset_map')
    reset_str = 'reset'
    rate = rospy.Rate(1)
    rate.sleep()
    pub.publish(reset_str)
    print "check"
    



if __name__ == '__main__':
    main()
